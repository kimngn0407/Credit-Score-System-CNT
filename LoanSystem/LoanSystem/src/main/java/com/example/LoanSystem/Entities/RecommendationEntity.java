package com.example.LoanSystem.Entities;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;


@Entity
@Table(name = "recommendations")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class RecommendationEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne @JoinColumn(name = "inference_run_id")
    private InferenceRunEntity inferenceRun;

    private String recCode;
    private String message;
    private BigDecimal expectedGain;
    private OffsetDateTime createdAt;
}