package com.example.LoanSystem.DTOs;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;


@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class PredictionDTO {
    private Long id;
    private Long inferenceRunId;
    private String decision;
    private BigDecimal probabilityApprove;
    private BigDecimal probabilityReject;
    private Integer creditScore;
    private OffsetDateTime createdAt;
}