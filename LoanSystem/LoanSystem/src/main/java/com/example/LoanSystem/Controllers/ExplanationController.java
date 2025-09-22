package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.ExplanationDTO;
import com.example.LoanSystem.DTOs.ExplanationDetailDTO;
import com.example.LoanSystem.Services.ExplanationService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/explanations")
@RequiredArgsConstructor
public class ExplanationController {
    private final ExplanationService service;

    @GetMapping("/run/{runId}")
    public List<ExplanationDTO> listByRun(@PathVariable Long runId){
        return service.byRun(runId);
    }

    @GetMapping("/{id}")
    public ExplanationDTO get(@PathVariable Long id){
        return service.get(id);
    }

    // Endpoint lấy explanation theo applicationId
    @GetMapping("/application/{appId}")
    public ExplanationDTO byApplication(@PathVariable Long appId) {
        return service.byApplication(appId);
    }
}
