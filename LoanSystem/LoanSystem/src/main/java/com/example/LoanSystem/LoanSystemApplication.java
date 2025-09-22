package com.example.LoanSystem;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.http.client.HttpClientAutoConfiguration;


@SpringBootApplication(
		exclude = { HttpClientAutoConfiguration.class } // chặn Spring auto-config Apache HttpClient
)
public class LoanSystemApplication {
	public static void main(String[] args) {
		SpringApplication.run(LoanSystemApplication.class, args);
	}
}
