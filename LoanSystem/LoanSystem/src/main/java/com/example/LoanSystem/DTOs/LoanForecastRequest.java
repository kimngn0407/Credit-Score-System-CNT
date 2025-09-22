package com.example.LoanSystem.DTOs;

import lombok.*;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LoanForecastRequest {
    private List<Double> features;
}

