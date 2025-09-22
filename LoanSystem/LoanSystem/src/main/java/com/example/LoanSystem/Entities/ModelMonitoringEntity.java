package com.example.LoanSystem.Entities;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Entity
@Table(name = "model_monitoring")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class ModelMonitoringEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String modelVersion;
    private BigDecimal accuracy;
    private BigDecimal auc;
    private BigDecimal driftScore;
    private OffsetDateTime measuredAt;
}