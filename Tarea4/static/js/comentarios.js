document.addEventListener('DOMContentLoaded', function() {
    console.log('Cargando comentarios...');
    cargarComentarios();
    
    // Configurar el formulario
    const form = document.getElementById('form-comentario');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Enviando comentario...');
            agregarComentario();
        });
    } else {
        console.error('No se encontró el formulario de comentarios');
    }
});

function cargarComentarios() {
    const avisoId = document.getElementById('aviso_id').value;
    console.log('Cargando comentarios para aviso:', avisoId);
    
    fetch(`/api/comentarios/${avisoId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta: ' + response.status);
            }
            return response.json();
        })
        .then(comentarios => {
            console.log('Comentarios recibidos:', comentarios);
            mostrarComentarios(comentarios);
        })
        .catch(error => {
            console.error('Error al cargar comentarios:', error);
            document.getElementById('lista-comentarios').innerHTML = '<p>Error al cargar comentarios</p>';
        });
}

function mostrarComentarios(comentarios) {
    const contenedor = document.getElementById('lista-comentarios');
    
    if (!comentarios || comentarios.length === 0) {
        contenedor.innerHTML = '<p>No hay comentarios aún.</p>';
        return;
    }
    
    let html = '';
    comentarios.forEach(comentario => {
        html += `
            <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
                <strong>${comentario.nombre}</strong> - ${comentario.fecha}
                <p>${comentario.texto}</p>
            </div>
        `;
    });
    
    contenedor.innerHTML = html;
    console.log('Comentarios mostrados:', comentarios.length);
}

function agregarComentario() {
    const avisoId = document.getElementById('aviso_id').value;
    const nombre = document.getElementById('nombre_comentario').value.trim();
    const texto = document.getElementById('texto_comentario').value.trim();
    
    console.log('Datos del comentario:', { avisoId, nombre, texto });
    

    document.getElementById('error-nombre').textContent = '';
    document.getElementById('error-texto').textContent = '';
    

    let errores = false;
    
    if (nombre.length < 3 || nombre.length > 80) {
        document.getElementById('error-nombre').textContent = 'Nombre debe tener entre 3 y 80 caracteres';
        errores = true;
    }
    
    if (texto.length < 5) {
        document.getElementById('error-texto').textContent = 'Comentario debe tener al menos 5 caracteres';
        errores = true;
    }
    
    if (errores) {
        console.log('Errores de validación');
        return;
    }
    
    // Enviar
    fetch('/api/comentarios/agregar', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({ 
            aviso_id: parseInt(avisoId), 
            nombre: nombre, 
            texto: texto 
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error HTTP: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('Respuesta del servidor:', data);
        if (data.success) {
            document.getElementById('form-comentario').reset();
            cargarComentarios(); // Recargar los comentarios
            alert('Comentario agregado correctamente!');
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error al enviar comentario:', error);
        alert('Error al enviar el comentario: ' + error.message);
    });
}