package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.AuditLogDTO;
import com.example.LoanSystem.Entities.AuditLogEntity;
import com.example.LoanSystem.Repositories.AuditLogRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AuditLogService {
    private final AuditLogRepository repo;

    public List<AuditLogDTO> byActor(String actor){
        return repo.findByActor(actor).stream().map(this::toDTO).toList();
    }

    private AuditLogDTO toDTO(AuditLogEntity e){
        return AuditLogDTO.builder()
                .id(e.getId())
                .actor(e.getActor())
                .action(e.getAction())
                .applicationId(e.getApplicationId())
                .inferenceRunId(e.getInferenceRunId())
                .payload(e.getPayload())
                .createdAt(e.getCreatedAt())
                .build();
    }
}