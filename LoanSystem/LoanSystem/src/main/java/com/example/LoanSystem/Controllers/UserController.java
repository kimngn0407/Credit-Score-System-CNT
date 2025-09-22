package com.example.LoanSystem.Controllers;

import com.example.LoanSystem.DTOs.UserDTO;
import com.example.LoanSystem.Services.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService service;
    @PostMapping public UserDTO create(@RequestBody UserDTO dto){return service.create(dto);}

    // Đăng ký tài khoản
    @PostMapping("/register")
    public UserDTO register(@RequestBody UserDTO dto) {
        return service.create(dto);
    }

    // Đăng nhập tài khoản
    @PostMapping("/login")
    public UserDTO login(@RequestBody UserDTO dto) {
        return service.login(dto.getUsername(), dto.getPasswordHash());
    }
    @GetMapping("/{id}") public UserDTO get(@PathVariable Long id){return service.get(id);}
    @GetMapping public List<UserDTO> list(){return service.list();}
    @PatchMapping("/{id}/theme")
    public UserDTO updateTheme(@PathVariable Long id,@RequestParam String theme){
        return service.updateTheme(id,theme);
    }
}