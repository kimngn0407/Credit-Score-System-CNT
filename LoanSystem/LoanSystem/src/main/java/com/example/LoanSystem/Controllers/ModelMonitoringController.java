package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.ModelMonitoringDTO;
import com.example.LoanSystem.Services.ModelMonitoringService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/monitoring")
@RequiredArgsConstructor
public class ModelMonitoringController {
    private final ModelMonitoringService service;
    @GetMapping("/version/{version}")
    public List<ModelMonitoringDTO> list(@PathVariable String version){
        return service.byVersion(version);
    }

    // Added to satisfy frontend expectation: GET /api/monitoring/metrics
    @GetMapping("/metrics")
    public Map<String, Object> metrics(){
        // Return a shape compatible with frontend: { accuracyOverTime: [{date, accuracy}] }
        List<ModelMonitoringDTO> all = service.byVersion("latest");
        var accuracyOverTime = all.stream()
                .map(m -> Map.of(
                        "date", m.getMeasuredAt().toLocalDate().toString(),
                        "accuracy", m.getAccuracy()
                ))
                .collect(Collectors.toList());
        return Map.of("accuracyOverTime", accuracyOverTime);
    }
}