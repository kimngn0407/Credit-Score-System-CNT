package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.BlockchainHashDTO;
import com.example.LoanSystem.Services.BlockchainService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/blockchain")
@RequiredArgsConstructor
public class BlockchainController {
    private final BlockchainService service;
    @GetMapping("/run/{runId}")
    public List<BlockchainHashDTO> list(@PathVariable Long runId){return service.byRun(runId);}
}