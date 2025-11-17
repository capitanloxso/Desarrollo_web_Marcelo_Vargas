package com.tarea4;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface NotaRepository extends JpaRepository<Nota, Integer> {
    @Query(value = "SELECT AVG(n.nota) FROM nota n WHERE n.aviso_id = :avisoId", nativeQuery = true)
    Double obtenerPromedio(Integer avisoId);
}