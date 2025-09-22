package com.example.LoanSystem.DTOs;

import lombok.*;

import java.time.OffsetDateTime;

@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class ExplanationDTO {
    private Long id;
    private Long inferenceRunId;
    private String method;
    private OffsetDateTime createdAt;
}
