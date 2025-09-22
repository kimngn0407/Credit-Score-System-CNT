package com.example.LoanSystem.DTOs;

import lombok.*;

import java.time.OffsetDateTime;

@Data
@NoArgsConstructor @AllArgsConstructor @Builder
public class AuditLogDTO {
    private Long id;
    private String actor;
    private String action;
    private Long applicationId;
    private Long inferenceRunId;
    private String payload;
    private OffsetDateTime createdAt;
}