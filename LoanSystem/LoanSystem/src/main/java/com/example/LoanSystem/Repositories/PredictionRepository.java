package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.PredictionEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PredictionRepository extends JpaRepository<PredictionEntity, Long> {
    List<PredictionEntity> findByInferenceRunId(Long inferenceRunId);
    // Đếm số lượng theo quyết định
    long countByDecision(String decision);

    // Tính điểm trung bình tín dụng
    @Query("SELECT AVG(p.creditScore) FROM PredictionEntity p")
    Double averageCreditScore();
    
    // Lấy prediction mới nhất theo application ID
    @Query("SELECT p FROM PredictionEntity p " +
           "JOIN p.inferenceRun ir " +
           "WHERE ir.application.id = :applicationId " +
           "ORDER BY p.createdAt DESC")
    List<PredictionEntity> findLatestByApplicationId(Long applicationId);
}

