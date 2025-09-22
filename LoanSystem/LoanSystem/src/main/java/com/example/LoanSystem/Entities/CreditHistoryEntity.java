package com.example.LoanSystem.Entities;

import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "credit_history")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class CreditHistoryEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne @JoinColumn(name = "user_id")
    private UserEntity user;

    @ManyToOne @JoinColumn(name = "application_id")
    private ApplicationEntity application;

    private OffsetDateTime date;
    private Integer score;
    private String decision;
}