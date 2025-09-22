package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.ApplicationDTO;
import com.example.LoanSystem.Entities.ApplicationEntity;
import com.example.LoanSystem.Entities.UserEntity;
import com.example.LoanSystem.Repositories.ApplicationRepository;
import com.example.LoanSystem.Repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.OffsetDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ApplicationService {
    private final ApplicationRepository repo;
    private final UserRepository userRepo;

    public ApplicationDTO create(Long userId, ApplicationDTO dto){
        UserEntity u=userRepo.findById(userId).orElseThrow();
        ApplicationEntity e = ApplicationEntity.builder()
                .user(u)
                .personAge(dto.getPersonAge())
                .personIncome(dto.getPersonIncome())
                .loanAmnt(dto.getLoanAmnt())
                .personHomeOwnership(dto.getPersonHomeOwnership())
                .cbPersonDefaultOnFile(dto.getCbPersonDefaultOnFile())
                .loanIntent(dto.getLoanIntent())
                .personEmpLength(dto.getPersonEmpLength())
                .cbPersonCredHistLength(dto.getCbPersonCredHistLength())
                .status("PENDING_INFERENCE")
                .createdAt(OffsetDateTime.now())
                .build();
        return toDTO(repo.save(e));
    }
    public List<ApplicationDTO> byUser(Long userId){
        return repo.findByUserId(userId).stream().map(this::toDTO).toList();
    }
    private ApplicationDTO toDTO(ApplicationEntity e){
        return ApplicationDTO.builder()
                .id(e.getId()).userId(e.getUser().getId())
                .personAge(e.getPersonAge()).personIncome(e.getPersonIncome())
                .loanAmnt(e.getLoanAmnt()).personHomeOwnership(e.getPersonHomeOwnership())
                .cbPersonDefaultOnFile(e.getCbPersonDefaultOnFile())
                .loanIntent(e.getLoanIntent()).personEmpLength(e.getPersonEmpLength())
                .cbPersonCredHistLength(e.getCbPersonCredHistLength())
                .status(e.getStatus()).createdAt(e.getCreatedAt()).build();
    }
}