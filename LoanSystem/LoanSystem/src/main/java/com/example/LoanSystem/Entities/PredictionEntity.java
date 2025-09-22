package com.example.LoanSystem.Entities;

import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Entity
@Table(name = "predictions")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class PredictionEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne @JoinColumn(name = "inference_run_id")
    private InferenceRunEntity inferenceRun;

    private String decision; // APPROVE / REJECT
    private BigDecimal probabilityApprove;
    private BigDecimal probabilityReject;
    private Integer creditScore;
    private OffsetDateTime createdAt;
}