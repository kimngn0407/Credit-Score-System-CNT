package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.CustomerLocationDTO;
import com.example.LoanSystem.Entities.CustomerLocationEntity;
import com.example.LoanSystem.Repositories.CustomerLocationRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class CustomerLocationService {
    private final CustomerLocationRepository repo;

    public List<CustomerLocationDTO> byProvince(String province){
        return repo.findByProvince(province).stream().map(this::toDTO).toList();
    }

    private CustomerLocationDTO toDTO(CustomerLocationEntity e){
        return CustomerLocationDTO.builder()
                .id(e.getId())
                .applicationId(e.getApplication().getId())
                .province(e.getProvince())
                .district(e.getDistrict())
                .lat(e.getLat())
                .lon(e.getLon())
                .build();
    }
}
