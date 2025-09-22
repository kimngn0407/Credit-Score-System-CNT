package com.example.LoanSystem.Entities;

import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "audit_logs")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class AuditLogEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String actor; // USER / STAFF / SYSTEM
    private String action; // CREATE_APP / PREDICT / EXPLAIN ...

    private Long applicationId;
    private Long inferenceRunId;

    @Column(columnDefinition = "jsonb")
    private String payload;

    private OffsetDateTime createdAt;
}