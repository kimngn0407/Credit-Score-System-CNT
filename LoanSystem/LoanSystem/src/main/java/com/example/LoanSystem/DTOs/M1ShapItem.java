package com.example.LoanSystem.DTOs;
import lombok.*;

@Data @NoArgsConstructor @AllArgsConstructor
public class M1ShapItem {
    private String featureName;
    private String featureValue; // có thể null
    private double shapValue;
    private int rank;
}