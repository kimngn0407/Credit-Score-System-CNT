package com.example.LoanSystem.Entities;
import jakarta.persistence.*;
import lombok.*;

import java.time.OffsetDateTime;

@Entity
@Table(name = "users")
@Data @NoArgsConstructor @AllArgsConstructor @Builder
public class UserEntity {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false, length = 50)
    private String username;

    @Column(name = "password_hash", nullable = false)
    private String passwordHash;

    @Column(name = "full_name", length = 100)
    private String fullName;

    @Column(unique = true, length = 100)
    private String email;

    @Column(nullable = false, length = 20)
    private String role; // USER, STAFF, ADMIN

    @Column(name = "theme_preference", length = 10)
    private String themePreference = "light";

    @Column(name = "created_at")
    private OffsetDateTime createdAt;
}
