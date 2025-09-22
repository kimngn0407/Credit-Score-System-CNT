package com.example.LoanSystem.Entities;
import jakarta.persistence.*;
import lombok.*;

import java.math.BigDecimal;

@Entity
@Table(name = "customer_locations")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class CustomerLocationEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne @JoinColumn(name = "application_id")
    private ApplicationEntity application;

    private String province;
    private String district;
    private BigDecimal lat;
    private BigDecimal lon;
}