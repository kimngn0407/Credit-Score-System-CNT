package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.AuditLogDTO;
import com.example.LoanSystem.Services.AuditLogService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/audit")
@RequiredArgsConstructor
public class AuditLogController {
    private final AuditLogService service;
    @GetMapping("/actor/{actor}")
    public List<AuditLogDTO> list(@PathVariable String actor){
        return service.byActor(actor);
    }
}