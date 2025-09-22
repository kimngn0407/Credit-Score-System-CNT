// com/example/LoanSystem/Config/AppConfig.java
package com.example.LoanSystem.Config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.client.SimpleClientHttpRequestFactory;

import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.http.client.reactive.ReactorClientHttpConnector;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import reactor.netty.http.client.HttpClient;
import io.netty.channel.ChannelOption;

import java.time.Duration;
import java.util.List;

@Configuration
public class AppConfig {

    @Bean
    public RestTemplate restTemplate(@Value("${model.api-key:}") String apiKey) {
        var f = new SimpleClientHttpRequestFactory();
        f.setConnectTimeout(10_000);
        f.setReadTimeout(15_000);

        RestTemplate rt = new RestTemplate(f);
        rt.getInterceptors().add((req, body, exec) -> {
            if (apiKey != null && !apiKey.isBlank()) {
                req.getHeaders().add("X-API-KEY", apiKey);
            }
            req.getHeaders().setAccept(List.of(MediaType.APPLICATION_JSON));
            req.getHeaders().setContentType(MediaType.APPLICATION_JSON);
            return exec.execute(req, body);
        });
        return rt;
    }

    // Provide a shared WebClient.Builder configured with headers and timeouts.
    @Bean
    public WebClient.Builder webClientBuilder(@Value("${model.api-key:}") String apiKey) {
        HttpClient httpClient = HttpClient.create()
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, 10_000)
                .responseTimeout(Duration.ofSeconds(15));

        return WebClient.builder()
                .clientConnector(new ReactorClientHttpConnector(httpClient))
                .defaultHeaders(h -> {
                    if (apiKey != null && !apiKey.isBlank()) {
                        h.add("X-API-KEY", apiKey);
                    }
                    h.setAccept(List.of(MediaType.APPLICATION_JSON));
                    h.setContentType(MediaType.APPLICATION_JSON);
                });
    }
    @Bean
    public WebMvcConfigurer corsConfigurer(@Value("${cors.allowed.origins:http://localhost:5173,http://localhost:5174}") String origins) {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                String[] allowed = origins.split(",");
                registry.addMapping("/**")
                        .allowedOrigins(allowed)
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                        .allowedHeaders("*")
                        .allowCredentials(true)
                        .maxAge(3600);
            }
        };
    }
}
