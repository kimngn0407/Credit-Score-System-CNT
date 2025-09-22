package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.AuditLogEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AuditLogRepository extends JpaRepository<AuditLogEntity, Long> {
    List<AuditLogEntity> findByActor(String actor);
    List<AuditLogEntity> findByApplicationId(Long applicationId);
    List<AuditLogEntity> findByInferenceRunId(Long inferenceRunId);
}
