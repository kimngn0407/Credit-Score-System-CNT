package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.ExplanationDetailDTO;
import com.example.LoanSystem.Entities.ExplanationDetailEntity;
import com.example.LoanSystem.Repositories.ExplanationDetailRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ExplanationDetailService {
    private final ExplanationDetailRepository repo;

    /** Lấy danh sách chi tiết theo id của bảng explanations */
    public List<ExplanationDetailDTO> findByExplanationId(Long explanationId) {
        return repo.findByExplanationId(explanationId)
                .stream()
                .map(this::toDTO)
                .toList();
    }

    /** Lấy một chi tiết cụ thể theo id */
    public ExplanationDetailDTO findById(Long id) {
        return repo.findById(id)
                .map(this::toDTO)
                .orElseThrow(() -> new RuntimeException("Explanation detail not found"));
    }

    private ExplanationDetailDTO toDTO(ExplanationDetailEntity e) {
        return ExplanationDetailDTO.builder()
                .id(e.getId())
                .explanationId(e.getExplanation().getId())
                .featureName(e.getFeatureName())
                .featureValue(e.getFeatureValue())
                .shapValue(e.getShapValue())
                .contributionPct(e.getContributionPct())
                .rank(e.getRank())
                .build();
    }
}

