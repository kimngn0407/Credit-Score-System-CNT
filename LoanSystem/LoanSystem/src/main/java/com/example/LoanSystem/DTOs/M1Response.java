package com.example.LoanSystem.DTOs;
import lombok.*;

import java.util.List;

@Data @NoArgsConstructor @AllArgsConstructor
public class M1Response {
    private String modelVersion;                 // -> JSON: model_version
    private String decision;
    private double probabilityApprove;           // -> JSON: probability_approve
    private double probabilityReject;            // -> JSON: probability_reject
    private int creditScore;                     // -> JSON: credit_score
    private List<M1ShapItem> shap;
    private Integer latencyMs;                   // -> JSON: latency_ms
}