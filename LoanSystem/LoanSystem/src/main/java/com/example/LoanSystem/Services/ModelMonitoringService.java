package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.ModelMonitoringDTO;
import com.example.LoanSystem.Entities.ModelMonitoringEntity;
import com.example.LoanSystem.Repositories.ModelMonitoringRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class ModelMonitoringService {
    private final ModelMonitoringRepository repo;

    public List<ModelMonitoringDTO> byVersion(String version){
        return repo.findByModelVersion(version).stream().map(this::toDTO).toList();
    }

    private ModelMonitoringDTO toDTO(ModelMonitoringEntity e){
        return ModelMonitoringDTO.builder()
                .id(e.getId())
                .modelVersion(e.getModelVersion())
                .accuracy(e.getAccuracy())
                .auc(e.getAuc())
                .driftScore(e.getDriftScore())
                .measuredAt(e.getMeasuredAt())
                .build();
    }
}
