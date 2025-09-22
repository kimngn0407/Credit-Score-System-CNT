package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.CustomerLocationDTO;
import com.example.LoanSystem.Services.CustomerLocationService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/customers")
@RequiredArgsConstructor
public class CustomerLocationController {
    private final CustomerLocationService service;
    @GetMapping("/province/{province}")
    public List<CustomerLocationDTO> list(@PathVariable String province){
        return service.byProvince(province);
    }
}