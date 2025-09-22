package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.RecommendationEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RecommendationRepository extends JpaRepository<RecommendationEntity, Long> {
    List<RecommendationEntity> findByInferenceRunId(Long inferenceRunId);
}
