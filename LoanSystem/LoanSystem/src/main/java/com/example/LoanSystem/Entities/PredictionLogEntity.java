package com.example.LoanSystem.Entities;
import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "prediction_logs")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class PredictionLogEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne @JoinColumn(name = "inference_run_id")
    private InferenceRunEntity inferenceRun;

    @Column(columnDefinition = "jsonb")
    private String inputPayload;

    @Column(columnDefinition = "jsonb")
    private String outputPayload;

    private Integer latencyMs;
    private OffsetDateTime createdAt;
}