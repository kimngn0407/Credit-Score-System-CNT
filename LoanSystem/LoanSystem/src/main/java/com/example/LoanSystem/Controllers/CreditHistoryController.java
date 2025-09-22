package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.CreditHistoryDTO;
import com.example.LoanSystem.Services.CreditHistoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/history")
@RequiredArgsConstructor
public class CreditHistoryController {
    private final CreditHistoryService service;

    @GetMapping("/{userId}")
    public List<CreditHistoryDTO> history(@PathVariable Long userId) {
        return service.historyByUser(userId);
    }
}

