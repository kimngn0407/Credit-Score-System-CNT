package com.example.LoanSystem.DTOs;

import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class RecommendationDTO {
    private Long id;
    private Long inferenceRunId;
    private String recCode;
    private String message;
    private BigDecimal expectedGain;
    private OffsetDateTime createdAt;
}