package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.ApplicationDTO;
import com.example.LoanSystem.Services.ApplicationService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/applications")
@CrossOrigin(origins = {"http://localhost:5173", "http://localhost:5174"})
@RequiredArgsConstructor
public class ApplicationController {
    private final ApplicationService service;
    @PostMapping("/{userId}")
    public ApplicationDTO create(@PathVariable Long userId,@RequestBody ApplicationDTO dto){
        return service.create(userId,dto);
    }
    @GetMapping("/user/{userId}")
    public List<ApplicationDTO> byUser(@PathVariable Long userId){return service.byUser(userId);}
}