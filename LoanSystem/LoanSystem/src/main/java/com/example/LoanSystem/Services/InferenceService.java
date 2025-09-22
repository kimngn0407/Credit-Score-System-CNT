package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.*;
import com.example.LoanSystem.Entities.*;
import com.example.LoanSystem.Repositories.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.LinkedHashMap;
import java.util.Map;

@Service
@RequiredArgsConstructor
@Slf4j
public class InferenceService {

    private final ExternalApiService externalApiService;
    private final ApplicationRepository appRepo;
    private final InferenceRunRepository runRepo;
    private final PredictionRepository predRepo;
    private final ExplanationRepository expRepo;
    private final ExplanationDetailRepository detRepo;
    private final PredictionLogRepository logRepo;
    private final RecommendationRepository recRepo;
    private final CurrencyConverterService currencyConverter;

    @Transactional
    public Long runFullPipeline(Long appId) {
        ApplicationEntity app = appRepo.findById(appId)
                .orElseThrow(() -> new IllegalArgumentException("Application not found: " + appId));

        // 0) mở run
        InferenceRunEntity run = new InferenceRunEntity();
        run.setApplication(app);
        run.setStatus("RUNNING");
        run.setModelVersion("1.0");
        run.setStartedAt(OffsetDateTime.now());
        run = runRepo.save(run);

        try {
            // 1) build features từ ApplicationEntity for credit-scoring-api
            M1Request m1Req = new M1Request();
            m1Req.setApplicationId(appId);
            
            // Map application data to credit scoring format (frontend now sends USD directly)
            Map<String, Object> features = new LinkedHashMap<>();
            features.put("person_age", app.getPersonAge());
            features.put("person_income", app.getPersonIncome().doubleValue());
            features.put("person_home_ownership", app.getPersonHomeOwnership());
            features.put("person_emp_length", app.getPersonEmpLength());
            features.put("loan_intent", app.getLoanIntent());
            features.put("loan_amnt", app.getLoanAmnt().doubleValue());
            features.put("cb_person_default_on_file", app.getCbPersonDefaultOnFile());
            features.put("cb_person_cred_hist_length", app.getCbPersonCredHistLength());
            
            log.info("Using USD values directly - Income: {} USD, Loan: {} USD", 
                    app.getPersonIncome(), app.getLoanAmnt());
            
            m1Req.setFeatures(features);

            // 2) CALL Credit Scoring API
            log.info("Calling credit scoring API for application {}", appId);
            long t0 = System.currentTimeMillis();
            M1Response m1Resp = externalApiService.callCreditScoring(m1Req);
            int latency = (int)(System.currentTimeMillis() - t0);

            if (m1Resp == null) {
                throw new RuntimeException("Credit scoring API returned null");
            }

            // 2.1) SAVE predictions
            PredictionEntity pred = new PredictionEntity();
            pred.setInferenceRun(run);
            pred.setDecision(m1Resp.getDecision());
            pred.setProbabilityApprove(BigDecimal.valueOf(m1Resp.getProbabilityApprove()));
            pred.setProbabilityReject(BigDecimal.valueOf(m1Resp.getProbabilityReject()));
            pred.setCreditScore(m1Resp.getCreditScore());
            pred.setCreatedAt(OffsetDateTime.now());
            predRepo.save(pred);

            // 2.2) SAVE explanations + details (temporarily disabled to unblock pipeline)
            // ExplanationEntity exp = new ExplanationEntity();
            // exp.setInferenceRun(run);
            // exp.setMethod("SHAP");
            // exp.setCreatedAt(OffsetDateTime.now());
            // exp = expRepo.save(exp);
            // if (m1Resp.getShap() != null) {
            //     int rankCounter = 1;
            //     for (M1ShapItem s : m1Resp.getShap()) {
            //         ExplanationDetailEntity d = new ExplanationDetailEntity();
            //         d.setExplanation(exp);
            //         d.setFeatureName(s.getFeatureName());
            //         d.setFeatureValue(s.getFeatureValue());
            //         d.setShapValue(BigDecimal.valueOf(s.getShapValue()));
            //         d.setRank(rankCounter++);
            //         detRepo.save(d);
            //     }
            // }

            // 2.3) SAVE prediction log
            // 2.3) SAVE prediction log (temporarily disabled to unblock pipeline)
            // PredictionLogEntity plog = new PredictionLogEntity();
            // plog.setInferenceRun(run);
            // plog.setInputPayload(toJsonSafe(features));
            // plog.setOutputPayload(toJsonSafe(m1Resp));
            // plog.setLatencyMs(latency);
            // plog.setCreatedAt(OffsetDateTime.now());
            // logRepo.save(plog);

            // 3) Call NLG service for explanation (optional)
            // try {
            //     String narrative = externalApiService.callCreditNlg(m1Resp, features);
            //     log.info("Generated narrative explanation for application {}", appId);
            //     // You could save this narrative to a separate table if needed
            // } catch (Exception e) {
            //     log.warn("Failed to generate narrative explanation for application {}: {}", appId, e.getMessage());
            // }

            // 4) đóng run
            run.setStatus("COMPLETED");
            run.setFinishedAt(OffsetDateTime.now());
            runRepo.save(run);

            return run.getId();

        } catch (Exception e) {
            log.error("Error in inference pipeline for application {}", appId, e);
            run.setStatus("FAILED");
            run.setFinishedAt(OffsetDateTime.now());
            runRepo.save(run);
            throw new RuntimeException("Inference pipeline failed: " + e.getMessage(), e);
        }
    }

    private static String toJsonSafe(Object o) {
        try {
            return new ObjectMapper().writeValueAsString(o);
        } catch (Exception e) {
            return "{}";
        }
    }
}