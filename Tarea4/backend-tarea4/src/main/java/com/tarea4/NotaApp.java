package com.tarea4;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import java.util.HashMap;
import java.util.Map;

@SpringBootApplication
@RestController
@RequestMapping("/api/notas")
public class NotaApp {

    public static void main(String[] args) {
        SpringApplication.run(NotaApp.class, args);
    }

    @Autowired
    private NotaRepository repositorio;


    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                // El asterisco "*" significa permitir a TODO el mundo
                registry.addMapping("/**")
                        .allowedOrigins("*")
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                        .allowedHeaders("*");
            }
        };
    }

    @GetMapping("/promedio/{avisoId}")
    public Map<String, Object> getPromedio(@PathVariable Integer avisoId) {
        Double promedio = repositorio.obtenerPromedio(avisoId);
        Map<String, Object> response = new HashMap<>();
        // Si es null devuelve "-", si no, redondea a 1 decimal
        response.put("promedio", promedio == null ? "-" : Math.round(promedio * 10.0) / 10.0);
        return response;
    }

    @PostMapping("/evaluar")
    public Map<String, Object> evaluar(@RequestBody Map<String, Integer> payload) {
        Nota nuevaNota = new Nota();
        nuevaNota.setAvisoId(payload.get("avisoId"));
        nuevaNota.setNota(payload.get("nota"));
        repositorio.save(nuevaNota);
        return getPromedio(payload.get("avisoId"));
    }
}