package com.example.LoanSystem.DTOs;

import java.util.List;
import lombok.*;
@Data @NoArgsConstructor @AllArgsConstructor
public class M2Response {
    private String decisionText;             // đoạn NLG tiếng Việt
    private List<M2Rec> recommendations;   // danh sách khuyến nghị
}