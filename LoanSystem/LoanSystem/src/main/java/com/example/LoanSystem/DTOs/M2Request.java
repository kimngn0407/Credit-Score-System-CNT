package com.example.LoanSystem.DTOs;
import lombok.*;

import java.util.Map;

@Data @NoArgsConstructor @AllArgsConstructor
public class M2Request {
    private Long applicationId;                  // -> JSON: application_id
    private Map<String, Object> applicationFeatures;  // -> JSON: application_features
    private M2Model1Out model1Output;            // -> JSON: model1_output
    private Integer topK;
}