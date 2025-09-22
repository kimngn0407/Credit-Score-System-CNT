package com.example.LoanSystem.Entities;

import jakarta.persistence.*;
import lombok.*;
import java.math.BigDecimal;

@Entity                                     // <== BẮT BUỘC
@Table(name = "explanation_details")        // map với tên bảng
@Data                                       // <== tự sinh getter/setter, toString
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ExplanationDetailEntity {

        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        @ManyToOne
        @JoinColumn(name = "explanation_id")
        private ExplanationEntity explanation;

        @Column(name = "feature_name")
        private String featureName;

        @Column(name = "feature_value")
        private String featureValue;

        @Column(name = "shap_value")
        private BigDecimal shapValue;

        @Column(name = "contribution_pct")
        private BigDecimal contributionPct;

        private Integer rank;
}
