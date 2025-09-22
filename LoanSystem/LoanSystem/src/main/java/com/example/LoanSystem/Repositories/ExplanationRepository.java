package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.ExplanationEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ExplanationRepository extends JpaRepository<ExplanationEntity, Long> {
    List<ExplanationEntity> findByInferenceRunId(Long inferenceRunId);
}