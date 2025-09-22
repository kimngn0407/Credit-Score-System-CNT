package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.CreditHistoryEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CreditHistoryRepository extends JpaRepository<CreditHistoryEntity, Long> {
    List<CreditHistoryEntity> findByUserId(Long userId);
    List<CreditHistoryEntity> findByApplicationId(Long applicationId);
}
