package com.example.LoanSystem.DTOs;
import lombok.*;

import java.util.List;

@Data @NoArgsConstructor @AllArgsConstructor
public class M2Model1Out {
    private String decision;
    private double probability_approve;
    private double probability_reject;
    private int credit_score;
    private List<M1ShapItem> topShap;
}
