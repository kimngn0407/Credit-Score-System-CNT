package com.example.LoanSystem.DTOs;

import lombok.*;

import java.math.BigDecimal;

@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class CustomerLocationDTO {
    private Long id;
    private Long applicationId;
    private String province;
    private String district;
    private BigDecimal lat;
    private BigDecimal lon;
}