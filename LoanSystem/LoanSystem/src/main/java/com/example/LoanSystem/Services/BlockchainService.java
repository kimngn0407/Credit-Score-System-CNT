package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.BlockchainHashDTO;
import com.example.LoanSystem.Entities.BlockchainHashEntity;
import com.example.LoanSystem.Repositories.BlockchainHashRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class BlockchainService {
    private final BlockchainHashRepository repo;

    public List<BlockchainHashDTO> byRun(Long runId){
        return repo.findByInferenceRunId(runId).stream().map(this::toDTO).toList();
    }

    private BlockchainHashDTO toDTO(BlockchainHashEntity e){
        return BlockchainHashDTO.builder()
                .id(e.getId())
                .inferenceRunId(e.getInferenceRun().getId())
                .hashValue(e.getHashValue())
                .chainRef(e.getChainRef())
                .createdAt(e.getCreatedAt())
                .build();
    }
}

