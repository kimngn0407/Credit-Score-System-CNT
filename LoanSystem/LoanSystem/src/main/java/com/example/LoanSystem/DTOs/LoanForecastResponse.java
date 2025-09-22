package com.example.LoanSystem.DTOs;

import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LoanForecastResponse {
    private Double prediction;
    private String version;
    private Double latencyMs;
}

