package com.example.LoanSystem.DTOs;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class DashboardSummaryDTO {
    private long totalApplications;
    private long approvedCount;
    private long rejectedCount;
    private double averageScore;
}