package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.BlockchainHashEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BlockchainHashRepository extends JpaRepository<BlockchainHashEntity, Long> {
    List<BlockchainHashEntity> findByInferenceRunId(Long inferenceRunId);
}
