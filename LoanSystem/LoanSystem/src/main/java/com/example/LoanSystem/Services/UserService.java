package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.UserDTO;
import com.example.LoanSystem.Entities.UserEntity;
import com.example.LoanSystem.Repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.OffsetDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository repo;

    public UserDTO login(String username, String password) {
        UserEntity user = repo.findByUsername(username).orElseThrow(() -> new RuntimeException("Invalid username or password"));
        // Nếu password lưu dạng hash, cần so sánh hash. Nếu lưu plain text thì so sánh trực tiếp.
        if (!user.getPasswordHash().equals(password)) {
            throw new RuntimeException("Invalid username or password");
        }
        return toDTO(user);
    }

    public UserDTO create(UserDTO dto) {
        // Validate required fields
        if (dto.getUsername() == null || dto.getUsername().trim().isEmpty()) {
            throw new RuntimeException("Username is required");
        }
        if (dto.getPasswordHash() == null || dto.getPasswordHash().trim().isEmpty()) {
            throw new RuntimeException("Password is required");
        }
        
        UserEntity e = UserEntity.builder()
                .username(dto.getUsername())
                .passwordHash(dto.getPasswordHash())
                .fullName(dto.getFullName())
                .email(dto.getEmail())
                .role(dto.getRole() != null ? dto.getRole() : "USER")
                .themePreference(dto.getThemePreference() != null ? dto.getThemePreference() : "light")
                .createdAt(OffsetDateTime.now())
                .build();
        return toDTO(repo.save(e));
    }
    
    public UserDTO get(Long id){ return repo.findById(id).map(this::toDTO).orElseThrow(); }
    public List<UserDTO> list(){ return repo.findAll().stream().map(this::toDTO).toList(); }
    public UserDTO updateTheme(Long id,String theme){
        UserEntity e=repo.findById(id).orElseThrow();
        e.setThemePreference(theme);
        return toDTO(repo.save(e));
    }
    private UserDTO toDTO(UserEntity e){
        return UserDTO.builder()
                .id(e.getId()).username(e.getUsername()).fullName(e.getFullName())
                .email(e.getEmail()).role(e.getRole())
                .themePreference(e.getThemePreference()).createdAt(e.getCreatedAt()).build();
    }
}
