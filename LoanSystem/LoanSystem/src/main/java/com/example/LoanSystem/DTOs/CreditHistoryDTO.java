package com.example.LoanSystem.DTOs;
import lombok.*;

import java.time.OffsetDateTime;


@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class CreditHistoryDTO {
    private Long id;
    private Long userId;
    private Long applicationId;
    private OffsetDateTime date;
    private Integer score;
    private String decision;
}