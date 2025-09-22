package com.example.LoanSystem.Services;
import com.example.LoanSystem.Entities.InferenceRunEntity;
import com.example.LoanSystem.Repositories.InferenceRunRepository;

import com.example.LoanSystem.DTOs.ExplanationDTO;
import com.example.LoanSystem.DTOs.ExplanationDetailDTO;
import com.example.LoanSystem.Entities.ExplanationDetailEntity;
import com.example.LoanSystem.Entities.ExplanationEntity;
import com.example.LoanSystem.Repositories.ExplanationDetailRepository;
import com.example.LoanSystem.Repositories.ExplanationRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ExplanationService {
    public ExplanationDTO get(Long id) {
        return repo.findById(id)
            .map(this::toDTO)
            .orElseThrow(() -> new RuntimeException("Explanation not found"));
    }
    private final ExplanationRepository repo;
    private final InferenceRunRepository inferenceRunRepository;

    public List<ExplanationDTO> byRun(Long runId){
        return repo.findByInferenceRunId(runId)
            .stream().map(this::toDTO).toList();
    }

    private ExplanationDTO toDTO(ExplanationEntity e){
        return ExplanationDTO.builder()
                .id(e.getId())
                .inferenceRunId(e.getInferenceRun().getId())
                .method(e.getMethod())
                .createdAt(e.getCreatedAt())
                .build();
    }

    public ExplanationDTO byApplication(Long appId) {
        List<InferenceRunEntity> runs = inferenceRunRepository.findByApplicationId(appId);
        if (runs.isEmpty()) {
            // Fallback: return an empty explanation instead of 500
            return ExplanationDTO.builder()
                    .id(null)
                    .inferenceRunId(null)
                    .method("SHAP")
                    .createdAt(null)
                    .build();
        }
        Long runId = runs.get(0).getId();
        List<ExplanationEntity> explanations = repo.findByInferenceRunId(runId);
        if (explanations.isEmpty()) {
            // Fallback: return an empty explanation instead of 500
            return ExplanationDTO.builder()
                    .id(null)
                    .inferenceRunId(runId)
                    .method("SHAP")
                    .createdAt(null)
                    .build();
        }
        return toDTO(explanations.get(0));
    }
}