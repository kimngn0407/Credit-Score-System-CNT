package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.PredictionDTO;
import com.example.LoanSystem.Services.InferenceService;
import com.example.LoanSystem.Services.PredictionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

// InferenceController.java
@RestController
@RequestMapping("/api/inference")
@RequiredArgsConstructor
public class InferenceController {
    private final InferenceService inferenceService;
    private final PredictionService predictionService;

    @PostMapping("/full/{appId}")
    public ResponseEntity<Map<String, Object>> runFull(@PathVariable Long appId) {
        Long runId = inferenceService.runFullPipeline(appId);
        return ResponseEntity.ok(Map.of("runId", runId));
    }

    @GetMapping("/result/{appId}")
    public ResponseEntity<PredictionDTO> getResult(@PathVariable Long appId) {
        PredictionDTO result = predictionService.getLatestByApplicationId(appId);
        if (result == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(result);
    }
}
