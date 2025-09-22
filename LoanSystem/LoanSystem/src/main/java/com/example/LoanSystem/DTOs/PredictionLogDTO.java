package com.example.LoanSystem.DTOs;
import lombok.*;

import java.time.OffsetDateTime;


@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class PredictionLogDTO {
    private Long id;
    private Long inferenceRunId;
    private String inputPayload;
    private String outputPayload;
    private Integer latencyMs;
    private OffsetDateTime createdAt;
}