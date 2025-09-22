package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.PredictionLogDTO;
import com.example.LoanSystem.Entities.PredictionLogEntity;
import com.example.LoanSystem.Repositories.PredictionLogRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PredictionLogService {
    private final PredictionLogRepository repo;

    public List<PredictionLogDTO> byRun(Long runId){
        return repo.findByInferenceRunId(runId).stream().map(this::toDTO).toList();
    }

    private PredictionLogDTO toDTO(PredictionLogEntity e){
        return PredictionLogDTO.builder()
                .id(e.getId())
                .inferenceRunId(e.getInferenceRun().getId())
                .inputPayload(e.getInputPayload())
                .outputPayload(e.getOutputPayload())
                .latencyMs(e.getLatencyMs())
                .createdAt(e.getCreatedAt())
                .build();
    }
}