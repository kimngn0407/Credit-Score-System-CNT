package com.example.LoanSystem.DTOs;

import lombok.*;

import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LoanExplainResponse {
    private Map<String, Double> explanation;
    private String version;
}

