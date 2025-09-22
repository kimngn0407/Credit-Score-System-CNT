package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.ModelMonitoringEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ModelMonitoringRepository extends JpaRepository<ModelMonitoringEntity, Long> {
    List<ModelMonitoringEntity> findByModelVersion(String modelVersion);
}
