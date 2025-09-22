package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.*;
import com.example.LoanSystem.Services.LoanForecastApiService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/loan-forecast")
@RequiredArgsConstructor
public class LoanForecastController {
    
    private final LoanForecastApiService loanForecastApiService;
    
    @PostMapping("/predict")
    public LoanForecastResponse predict(@RequestBody LoanForecastRequest request) {
        return loanForecastApiService.predict(request.getFeatures());
    }
    
    @PostMapping("/explain")
    public LoanExplainResponse explain(@RequestBody LoanForecastRequest request) {
        return loanForecastApiService.explain(request.getFeatures());
    }
    
    @PostMapping("/optimize")
    public LoanOptimizeResponse optimize(@RequestBody LoanForecastRequest request) {
        return loanForecastApiService.optimize(request.getFeatures());
    }
    
    @GetMapping("/health")
    public String healthCheck() {
        return loanForecastApiService.healthCheck();
    }
}
