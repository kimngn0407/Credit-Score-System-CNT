package com.example.LoanSystem.Entities;
import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "explanations")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class ExplanationEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne @JoinColumn(name = "inference_run_id")
    private InferenceRunEntity inferenceRun;

    private String method; // SHAP/LIME
    private OffsetDateTime createdAt;
}