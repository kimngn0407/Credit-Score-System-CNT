package com.example.LoanSystem.DTOs;
import lombok.*;

import java.util.Map;

@Data @NoArgsConstructor @AllArgsConstructor
public class M1Request {
    private Long applicationId;
    private Map<String, Object> features;
}