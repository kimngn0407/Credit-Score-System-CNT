package com.example.LoanSystem.Repositories;
import com.example.LoanSystem.Entities.ApplicationEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;


@Repository
public interface ApplicationRepository extends JpaRepository<ApplicationEntity, Long> {
    List<ApplicationEntity> findByUserId(Long userId);
    List<ApplicationEntity> findByStatus(String status);
}
