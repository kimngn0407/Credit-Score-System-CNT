package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.PredictionDTO;
import com.example.LoanSystem.Entities.PredictionEntity;
import com.example.LoanSystem.Repositories.PredictionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PredictionService {
    private final PredictionRepository repo;
    public List<PredictionDTO> byRun(Long runId){
        return repo.findByInferenceRunId(runId)
                .stream().map(this::toDTO).toList();
    }
    
    public PredictionDTO getLatestByApplicationId(Long applicationId) {
        List<PredictionEntity> predictions = repo.findLatestByApplicationId(applicationId);
        if (predictions.isEmpty()) {
            return null;
        }
        return toDTO(predictions.get(0));
    }
    
    private PredictionDTO toDTO(PredictionEntity e){
        return PredictionDTO.builder()
                .id(e.getId()).inferenceRunId(e.getInferenceRun().getId())
                .decision(e.getDecision())
                .probabilityApprove(e.getProbabilityApprove())
                .probabilityReject(e.getProbabilityReject())
                .creditScore(e.getCreditScore())
                .createdAt(e.getCreatedAt()).build();
    }
}

