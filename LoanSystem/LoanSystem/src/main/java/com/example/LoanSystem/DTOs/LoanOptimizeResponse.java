package com.example.LoanSystem.DTOs;

import lombok.*;

import java.util.Map;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LoanOptimizeResponse {
    private Map<String, String> suggestions;
    private String version;
}

