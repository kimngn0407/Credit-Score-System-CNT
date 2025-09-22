package com.example.LoanSystem.Entities;
import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "inference_runs")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class InferenceRunEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne @JoinColumn(name = "application_id")
    private ApplicationEntity application;

    private OffsetDateTime startedAt;
    private OffsetDateTime finishedAt;
    private String status; // RUNNING
    private String modelVersion;
}