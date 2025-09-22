package com.example.LoanSystem.DTOs;
import lombok.*;

@Data @NoArgsConstructor @AllArgsConstructor
public class M2Rec {
    private String recCode;                      // -> JSON: rec_code
    private String message;
    private Double expectedGain;
}
