package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

@Service
@Slf4j
public class ExternalApiService {

    private WebClient creditScoringWebClient;
    private WebClient creditNlgWebClient;
    private final WebClient.Builder webClientBuilder;
    private final String model1BaseUrl;
    private final String model2BaseUrl;

    public ExternalApiService(WebClient.Builder webClientBuilder,
                            @Value("${model1.base-url}") String model1BaseUrl,
                            @Value("${model2.base-url}") String model2BaseUrl) {
        this.webClientBuilder = webClientBuilder;
        this.model1BaseUrl = model1BaseUrl;
        this.model2BaseUrl = model2BaseUrl;
    }

    @jakarta.annotation.PostConstruct
    public void initClients() {
        this.creditScoringWebClient = webClientBuilder.baseUrl(model1BaseUrl).build();
        // TODO: Uncomment when GPU is available for credit-nlg-service
        // this.creditNlgWebClient = webClientBuilder.baseUrl(model2BaseUrl).build();
        log.info("ExternalApiService initialized - NLG service disabled");
    }

    /**
     * Call Credit Scoring API to predict loan application
     */
    public M1Response callCreditScoring(M1Request request) {
        try {
            log.info("Calling credit scoring API with request: {}", request);
            
            // The FastAPI service expects a flat JSON body matching CreditApplication (feature map),
            // and responds with fields: score, approved, decision_en, decision_vi, threshold, shap, shap_bias, shap_sum_check.
            // We map that response into our internal M1Response for downstream usage.

            Mono<Map> response = creditScoringWebClient
                    .post()
                    .uri("/predict")
                    .bodyValue(request.getFeatures())
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofSeconds(30));

            @SuppressWarnings("unchecked")
            Map<String, Object> raw = (Map<String, Object>) response.block();

            if (raw == null) {
                throw new RuntimeException("Credit scoring API returned null body");
            }

            double score = toDouble(raw.get("score")); // default probability (xác suất vỡ nợ)
            boolean approved = toBoolean(raw.get("approved"));
            double probabilityReject = clamp01(score);  // score = probability of default
            double probabilityApprove = clamp01(1.0 - score);
            String decision = approved ? "APPROVE" : "REJECT";
            int creditScore = (int) Math.round(probabilityApprove * 1000.0);

            @SuppressWarnings("unchecked")
            Map<String, Object> shapMap = (Map<String, Object>) raw.get("shap");
            List<M1ShapItem> shapList = new ArrayList<>();
            if (shapMap != null) {
                // rank by absolute SHAP value desc
                shapMap.entrySet().stream()
                        .sorted(Comparator.comparingDouble(e -> -Math.abs(toDouble(e.getValue()))))
                        .forEachOrdered(entry -> {
                            M1ShapItem item = new M1ShapItem();
                            item.setFeatureName(entry.getKey());
                            item.setFeatureValue(null);
                            item.setShapValue(toDouble(entry.getValue()));
                            item.setRank(shapList.size() + 1);
                            shapList.add(item);
                        });
            }

            M1Response mapped = new M1Response();
            mapped.setModelVersion("lightgbm-1");
            mapped.setDecision(decision);
            mapped.setProbabilityApprove(probabilityApprove);
            mapped.setProbabilityReject(probabilityReject);
            mapped.setCreditScore(creditScore);
            mapped.setShap(shapList);
            // latencyMs is filled by caller if needed

            log.info("Credit scoring mapped response: decision={}, score={}, pApprove={}, pReject={}",
                    decision, score, probabilityApprove, probabilityReject);
            return mapped;
            
        } catch (Exception e) {
            log.error("Error calling credit scoring API", e);
            throw new RuntimeException("Failed to call credit scoring API: " + e.getMessage(), e);
        }
    }

    private static boolean toBoolean(Object value) {
        if (value instanceof Boolean b) return b;
        if (value instanceof String s) return Boolean.parseBoolean(s);
        if (value instanceof Number n) return n.intValue() != 0;
        return false;
    }

    private static double toDouble(Object value) {
        if (value instanceof Number n) return n.doubleValue();
        if (value instanceof String s) {
            try { return Double.parseDouble(s); } catch (Exception ignored) { }
        }
        return 0.0;
    }

    private static double clamp01(double v) {
        if (v < 0.0) return 0.0;
        if (v > 1.0) return 1.0;
        return v;
    }

    /**
     * Call Credit NLG API to generate explanation
     */
    public String callCreditNlg(M1Response scoringResult, Map<String, Object> profileRaw) {
        // TODO: Uncomment when GPU is available for credit-nlg-service
        /*
        try {
            log.info("Calling credit NLG API for explanation");
            
            // Prepare NLG request
            var nlgRequest = Map.of(
                "model_output", scoringResult,
                "profile_raw", profileRaw,
                "top_k", 5
            );
            
            var response = creditNlgWebClient
                    .post()
                    .uri("/nlg")
                    .bodyValue(nlgRequest)
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofSeconds(60));
            
            @SuppressWarnings("unchecked")
            Map<String, Object> result = (Map<String, Object>) response.block();
            String narrative = (String) result.get("narrative_vi");
            
            log.info("Credit NLG API response received");
            return narrative != null ? narrative : "Không thể tạo giải thích cho kết quả này.";
            
        } catch (Exception e) {
            log.error("Error calling credit NLG API", e);
            return "Lỗi khi tạo giải thích: " + e.getMessage();
        }
        */
        
        // Temporary fallback explanation without NLG service
        log.info("Using fallback explanation (NLG service disabled)");
        String decision = scoringResult.getDecision();
        double probabilityApprove = scoringResult.getProbabilityApprove();
        
        if ("APPROVE".equals(decision)) {
            return String.format("Đơn vay được phê duyệt với xác suất %.1f%%. " +
                "Khách hàng có hồ sơ tín dụng tốt và đủ điều kiện vay.", 
                probabilityApprove * 100);
        } else {
            return String.format("Đơn vay không được phê duyệt. " +
                "Xác suất rủi ro cao (%.1f%%). Khuyến nghị cải thiện hồ sơ tín dụng.", 
                (1 - probabilityApprove) * 100);
        }
    }

    /**
     * Health check for external APIs
     */
    public boolean checkCreditScoringHealth() {
        try {
            var response = creditScoringWebClient
                    .get()
                    .uri("/healthz")
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofSeconds(10));
            
            @SuppressWarnings("unchecked")
            Map<String, Object> result = (Map<String, Object>) response.block();
            return "ok".equals(result.get("status"));
        } catch (Exception e) {
            log.warn("Credit scoring API health check failed", e);
            return false;
        }
    }

    public boolean checkCreditNlgHealth() {
        // TODO: Uncomment when GPU is available for credit-nlg-service
        /*
        try {
            var response = creditNlgWebClient
                    .get()
                    .uri("/healthz")
                    .retrieve()
                    .bodyToMono(Map.class)
                    .timeout(Duration.ofSeconds(10));
            
            @SuppressWarnings("unchecked")
            Map<String, Object> result = (Map<String, Object>) response.block();
            return "ok".equals(result.get("status"));
        } catch (Exception e) {
            log.warn("Credit NLG API health check failed", e);
            return false;
        }
        */
        
        // Temporary: Return true since NLG service is disabled
        log.info("Credit NLG service disabled - returning healthy status");
        return true;
    }
}