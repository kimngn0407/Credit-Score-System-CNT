package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.PredictionLogDTO;
import com.example.LoanSystem.Services.PredictionLogService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/prediction-logs")
@RequiredArgsConstructor
public class PredictionLogController {
    private final PredictionLogService service;
    @GetMapping("/run/{runId}")
    public List<PredictionLogDTO> list(@PathVariable Long runId){return service.byRun(runId);}
}
