package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.DashboardSummaryDTO;
import com.example.LoanSystem.Repositories.ApplicationRepository;
import com.example.LoanSystem.Repositories.PredictionRepository;
import com.example.LoanSystem.Services.CurrencyConverterService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/dashboard")
@CrossOrigin(origins = {"http://localhost:5173", "http://localhost:5174"})
@RequiredArgsConstructor
public class DashboardController {
    private final ApplicationRepository applicationRepo;
    private final PredictionRepository predictionRepo;
    private final CurrencyConverterService currencyConverter;

    @GetMapping("/summary")
    public DashboardSummaryDTO getSummary() {
        long totalApplications = applicationRepo.count();
        long approvedCount = predictionRepo.countByDecision("approve");
        long rejectedCount = predictionRepo.countByDecision("reject");
        Double averageScore = predictionRepo.averageCreditScore();
        if (averageScore == null) averageScore = 0.0;
        return DashboardSummaryDTO.builder()
                .totalApplications(totalApplications)
                .approvedCount(approvedCount)
                .rejectedCount(rejectedCount)
                .averageScore(averageScore)
                .build();
    }

    @GetMapping("/currency-info")
    public Map<String, Object> getCurrencyInfo() {
        return Map.of(
            "currency", "USD",
            "note", "System now uses USD throughout - frontend, backend, and model."
        );
    }
}