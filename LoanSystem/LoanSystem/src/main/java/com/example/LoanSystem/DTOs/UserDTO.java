package com.example.LoanSystem.DTOs;
import lombok.*;

import java.time.OffsetDateTime;

@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class UserDTO {
    private Long id;
    private String username;
    private String fullName;
    private String email;
    private String role;
    private String passwordHash;
    private String themePreference;
    private OffsetDateTime createdAt;
}