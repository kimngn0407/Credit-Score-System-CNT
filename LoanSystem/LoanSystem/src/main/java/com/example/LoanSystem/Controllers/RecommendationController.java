package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.RecommendationDTO;
import com.example.LoanSystem.Services.RecommendationService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/recommendations")
@RequiredArgsConstructor
public class RecommendationController {
    private final RecommendationService service;
    @GetMapping("/run/{runId}")
    public List<RecommendationDTO> list(@PathVariable Long runId){return service.byRun(runId);}

    // Endpoint lấy recommendation theo applicationId
    @GetMapping("/application/{appId}")
    public List<RecommendationDTO> byApplication(@PathVariable Long appId) {
        return service.byApplication(appId);
    }
}
