package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.PredictionLogEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PredictionLogRepository extends JpaRepository<PredictionLogEntity, Long> {
    List<PredictionLogEntity> findByInferenceRunId(Long inferenceRunId);
}
