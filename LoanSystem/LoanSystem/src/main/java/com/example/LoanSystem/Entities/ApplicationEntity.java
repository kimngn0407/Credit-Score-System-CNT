package com.example.LoanSystem.Entities;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Entity
@Table(name = "applications")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class ApplicationEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne @JoinColumn(name = "user_id")
    private UserEntity user;

    private Integer personAge;
    private BigDecimal personIncome;
    private BigDecimal loanAmnt;
    private String personHomeOwnership;
    private String cbPersonDefaultOnFile; // Y/N
    private String loanIntent;
    private BigDecimal personEmpLength;
    private Integer cbPersonCredHistLength;

    private String status; // PENDING_INFERENCE

    @Column(name = "created_at")
    private OffsetDateTime createdAt;
}