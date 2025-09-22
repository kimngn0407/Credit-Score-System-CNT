package com.example.LoanSystem.DTOs;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;


@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class ModelMonitoringDTO {
    private Long id;
    private String modelVersion;
    private BigDecimal accuracy;
    private BigDecimal auc;
    private BigDecimal driftScore;
    private OffsetDateTime measuredAt;
}