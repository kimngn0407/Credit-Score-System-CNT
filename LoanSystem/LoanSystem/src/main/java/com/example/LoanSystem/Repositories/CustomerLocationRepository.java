package com.example.LoanSystem.Repositories;

import com.example.LoanSystem.Entities.CustomerLocationEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CustomerLocationRepository extends JpaRepository<CustomerLocationEntity, Long> {
    List<CustomerLocationEntity> findByApplicationId(Long applicationId);
    List<CustomerLocationEntity> findByProvince(String province);
}
