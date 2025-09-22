package com.example.LoanSystem.DTOs;
import lombok.*;

import java.math.BigDecimal;


@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class ExplanationDetailDTO {
    private Long id;
    private Long explanationId;
    private String featureName;
    private String featureValue;
    private BigDecimal shapValue;
    private BigDecimal contributionPct;
    private Integer rank;
}