package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.InferenceRunEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface InferenceRunRepository extends JpaRepository<InferenceRunEntity, Long> {
    List<InferenceRunEntity> findByApplicationId(Long applicationId);
}
