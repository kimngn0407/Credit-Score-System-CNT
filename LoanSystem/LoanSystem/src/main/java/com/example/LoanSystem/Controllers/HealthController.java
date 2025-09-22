package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.Services.ExternalApiService;
import lombok.RequiredArgsConstructor;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/health")
@RequiredArgsConstructor
public class HealthController {

    private final ExternalApiService externalApiService;
    private final JdbcTemplate jdbcTemplate;

    @GetMapping
    public Map<String, Object> healthCheck() {
        boolean scoringApiHealth = externalApiService.checkCreditScoringHealth();
        boolean nlgApiHealth = externalApiService.checkCreditNlgHealth();

        boolean dbUp = false;
        try {
            jdbcTemplate.queryForObject("SELECT 1", Integer.class);
            dbUp = true;
        } catch (Exception ignored) { }

        String status = (scoringApiHealth && nlgApiHealth && dbUp) ? "UP" : "DEGRADED";

        return Map.of(
            "status", status,
            "services", Map.of(
                "database", dbUp ? "UP" : "DOWN",
                "credit-scoring-api", scoringApiHealth ? "UP" : "DOWN",
                "credit-nlg-service", nlgApiHealth ? "UP" : "DOWN"
            ),
            "timestamp", java.time.Instant.now()
        );
    }
}