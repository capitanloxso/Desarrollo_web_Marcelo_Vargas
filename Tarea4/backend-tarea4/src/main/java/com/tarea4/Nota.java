package com.tarea4;

import jakarta.persistence.*;

@Entity
@Table(name = "nota")
public class Nota {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "aviso_id", nullable = false)
    private Integer avisoId;

    @Column(nullable = false)
    private Integer nota;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public Integer getAvisoId() { return avisoId; }
    public void setAvisoId(Integer avisoId) { this.avisoId = avisoId; }
    public Integer getNota() { return nota; }
    public void setNota(Integer nota) { this.nota = nota; }
}