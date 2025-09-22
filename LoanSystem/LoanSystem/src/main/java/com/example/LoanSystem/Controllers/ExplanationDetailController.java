package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.ExplanationDetailDTO;
import com.example.LoanSystem.Services.ExplanationDetailService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/explanation-details")
@RequiredArgsConstructor
public class ExplanationDetailController {
    private final ExplanationDetailService service;

    // Danh sách tất cả detail của một explanation
    @GetMapping("/explanation/{explanationId}")
    public List<ExplanationDetailDTO> getByExplanation(@PathVariable Long explanationId) {
        return service.findByExplanationId(explanationId);
    }

    // Lấy 1 record chi tiết cụ thể
    @GetMapping("/{id}")
    public ExplanationDetailDTO getOne(@PathVariable Long id) {
        return service.findById(id);
    }
}
