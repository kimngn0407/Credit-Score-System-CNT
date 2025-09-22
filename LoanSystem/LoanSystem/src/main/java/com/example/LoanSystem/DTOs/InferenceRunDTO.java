package com.example.LoanSystem.DTOs;

import lombok.*;

import java.time.OffsetDateTime;

@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class InferenceRunDTO {
    private Long id;
    private Long applicationId;
    private OffsetDateTime startedAt;
    private OffsetDateTime finishedAt;
    private String status;
    private String modelVersion;
}