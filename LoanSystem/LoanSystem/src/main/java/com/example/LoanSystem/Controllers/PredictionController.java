package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.PredictionDTO;
import com.example.LoanSystem.Services.PredictionService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/predictions")
@RequiredArgsConstructor
public class PredictionController {
    private final PredictionService service;
    @GetMapping("/run/{runId}")
    public List<PredictionDTO> list(@PathVariable Long runId){return service.byRun(runId);}
}