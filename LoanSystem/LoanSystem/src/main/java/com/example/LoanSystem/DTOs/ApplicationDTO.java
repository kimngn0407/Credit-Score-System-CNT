package com.example.LoanSystem.DTOs;

import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class ApplicationDTO {
    private Long id;
    private Long userId;
    private Integer personAge;
    private BigDecimal personIncome;
    private BigDecimal loanAmnt;
    private String personHomeOwnership;
    private String cbPersonDefaultOnFile;
    private String loanIntent;
    private BigDecimal personEmpLength;
    private Integer cbPersonCredHistLength;
    private String status;
    private OffsetDateTime createdAt;
}