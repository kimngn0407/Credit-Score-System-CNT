package com.example.LoanSystem.DTOs;
import lombok.*;

import java.time.OffsetDateTime;


@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class BlockchainHashDTO {
    private Long id;
    private Long inferenceRunId;
    private String hashValue;
    private String chainRef;
    private OffsetDateTime createdAt;
}