package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.ExplanationDetailEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ExplanationDetailRepository extends JpaRepository<ExplanationDetailEntity, Long> {
    List<ExplanationDetailEntity> findByExplanationId(Long explanationId);
}