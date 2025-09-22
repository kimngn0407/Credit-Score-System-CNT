package com.example.LoanSystem.Services;

import com.example.LoanSystem.DTOs.*;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Service
@RequiredArgsConstructor
public class LoanForecastApiService {
    
    private final RestTemplate restTemplate;
    
    @Value("${loan.forecast.api.url:http://localhost:8000}")
    private String apiUrl;
    
    @Value("${loan.forecast.api.token:}")
    private String apiToken;
    
    public LoanForecastResponse predict(List<Double> features) {
        String url = apiUrl + "/predict";
        
        LoanForecastRequest request = LoanForecastRequest.builder()
                .features(features)
                .build();
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        if (!apiToken.isEmpty()) {
            headers.set("X-API-Key", apiToken);
        }
        
        HttpEntity<LoanForecastRequest> entity = new HttpEntity<>(request, headers);
        
        ResponseEntity<LoanForecastResponse> response = restTemplate.exchange(
                url, HttpMethod.POST, entity, LoanForecastResponse.class);
        
        return response.getBody();
    }
    
    public LoanExplainResponse explain(List<Double> features) {
        String url = apiUrl + "/explain";
        
        LoanForecastRequest request = LoanForecastRequest.builder()
                .features(features)
                .build();
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        if (!apiToken.isEmpty()) {
            headers.set("X-API-Key", apiToken);
        }
        
        HttpEntity<LoanForecastRequest> entity = new HttpEntity<>(request, headers);
        
        ResponseEntity<LoanExplainResponse> response = restTemplate.exchange(
                url, HttpMethod.POST, entity, LoanExplainResponse.class);
        
        return response.getBody();
    }
    
    public LoanOptimizeResponse optimize(List<Double> features) {
        String url = apiUrl + "/optimize";
        
        LoanForecastRequest request = LoanForecastRequest.builder()
                .features(features)
                .build();
        
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        if (!apiToken.isEmpty()) {
            headers.set("X-API-Key", apiToken);
        }
        
        HttpEntity<LoanForecastRequest> entity = new HttpEntity<>(request, headers);
        
        ResponseEntity<LoanOptimizeResponse> response = restTemplate.exchange(
                url, HttpMethod.POST, entity, LoanOptimizeResponse.class);
        
        return response.getBody();
    }
    
    public String healthCheck() {
        String url = apiUrl + "/health";
        ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
        return response.getBody();
    }
}

