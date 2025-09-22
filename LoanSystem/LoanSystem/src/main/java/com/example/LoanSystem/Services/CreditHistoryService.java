package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.CreditHistoryDTO;
import com.example.LoanSystem.Entities.CreditHistoryEntity;
import com.example.LoanSystem.Repositories.CreditHistoryRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class CreditHistoryService {
    private final CreditHistoryRepository repo;

    public List<CreditHistoryDTO> historyByUser(Long userId) {
        return repo.findByUserId(userId).stream().map(this::toDTO).toList();
    }

    private CreditHistoryDTO toDTO(CreditHistoryEntity e) {
        return CreditHistoryDTO.builder()
                .id(e.getId())
                .userId(e.getUser().getId())
                .applicationId(e.getApplication().getId())
                .date(e.getDate())
                .score(e.getScore())
                .decision(e.getDecision())
                .build();
    }
}

