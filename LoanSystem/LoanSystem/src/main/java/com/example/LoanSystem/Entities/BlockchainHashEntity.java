package com.example.LoanSystem.Entities;
import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "blockchain_hashes")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class BlockchainHashEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne @JoinColumn(name = "inference_run_id")
    private InferenceRunEntity inferenceRun;

    private String hashValue;
    private String chainRef;
    private OffsetDateTime createdAt;
}