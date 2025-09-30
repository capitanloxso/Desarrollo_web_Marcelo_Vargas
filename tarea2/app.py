from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Region, Comuna, AvisoAdopcion, Foto, ContactarPor
from config import Config
from datetime import datetime
from sqlalchemy.orm import joinedload
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


# Configuración de archivos permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    
    # Obtener últimos 5 avisos para la portada
    ultimos_avisos = AvisoAdopcion.query.order_by(AvisoAdopcion.fecha_ingreso.desc()).limit(5).all()
    
    return render_template('index.html', avisos=ultimos_avisos)




@app.route('/agregar', methods=['GET', 'POST'])
def agregar_aviso():
    
    if request.method == 'GET':
        regiones = Region.query.all()
        return render_template('agregar.html', regiones=regiones)
    
    
    # Procesar formulario POST
    try:
        
        # Validaciones del servidor
        errors = []
        
        
        # Validar campos obligatorios
        required_fields = ['region', 'comuna', 'nombre', 'email', 'tipo', 
                          'cantidad', 'edad', 'unidad_medida', 'fecha_entrega']
        
        for field in required_fields:
            if not request.form.get(field):
                errors.append(f"El campo {field} es obligatorio")
        
        
        # Validar email
        email = request.form.get('email')
        if email and '@' not in email:
            errors.append("El email no es válido")
        
        
        # Validar celular si existe
        celular = request.form.get('celular')
        if celular and not celular.startswith('+569'):
            errors.append("El celular debe comenzar con +569")
        
        
        if errors:
            flash('; '.join(errors), 'error')
            regiones = Region.query.all()
            return render_template('agregar.html', regiones=regiones, form_data=request.form)
        
        
        # Crear nuevo aviso
        nuevo_aviso = AvisoAdopcion(
            fecha_ingreso=datetime.now(),
            comuna_id=request.form['comuna'],
            sector=request.form.get('sector'),
            nombre=request.form['nombre'],
            email=request.form['email'],
            celular=request.form.get('celular'),
            tipo=request.form['tipo'],
            cantidad=int(request.form['cantidad']),
            edad=int(request.form['edad']),
            unidad_medida=request.form['unidad_medida'],
            fecha_entrega=datetime.fromisoformat(request.form['fecha_entrega'].replace('T', ' ')),
            descripcion=request.form.get('descripcion')
        )
        
        db.session.add(nuevo_aviso)
        db.session.flush()  # Para obtener el ID
        
        
        # Procesar formas de contacto
        contactos = request.form.getlist('contactar_por_nombre')
        identificadores = request.form.getlist('contactar_por_identificador')
        
        for nombre, identificador in zip(contactos, identificadores):
            if nombre and identificador:
                contacto = ContactarPor(
                    nombre=nombre,
                    identificador=identificador,
                    actividad_id=nuevo_aviso.id
                )
                db.session.add(contacto)
        
        
        # Procesar fotos
        if 'fotos' in request.files:
            fotos = request.files.getlist('fotos')
            
            for foto in fotos:
                if foto and allowed_file(foto.filename):
                    filename = secure_filename(foto.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    foto.save(filepath)
                    
                    nueva_foto = Foto(
                        ruta_archivo=f'uploads/{filename}',
                        nombre_archivo=filename,
                        actividad_id=nuevo_aviso.id
                    )
                    db.session.add(nueva_foto)
        
        
        db.session.commit()
        flash('Aviso de adopción agregado correctamente!', 'success')
        return redirect(url_for('index'))
        
        
    except Exception as e:
        
        db.session.rollback()
        flash(f'Error al agregar aviso: {str(e)}', 'error')
        regiones = Region.query.all()
        return render_template('agregar.html', regiones=regiones, form_data=request.form)




@app.route('/comunas/<int:region_id>')
def get_comunas(region_id):
    
    comunas = Comuna.query.filter_by(region_id=region_id).all()
    
    return jsonify([{'id': c.id, 'nombre': c.nombre} for c in comunas])




@app.route('/listar')
def listar_avisos():
    
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    
    avisos = AvisoAdopcion.query.order_by(AvisoAdopcion.fecha_ingreso.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    
    return render_template('listar.html', avisos=avisos)



@app.route('/aviso/<int:aviso_id>')
def detalle_aviso(aviso_id):
    
    aviso = AvisoAdopcion.query.options(
        joinedload(AvisoAdopcion.comuna).joinedload(Comuna.region),
        joinedload(AvisoAdopcion.fotos),
        joinedload(AvisoAdopcion.contactos)
    ).get_or_404(aviso_id)
    
    return render_template('detalle.html', aviso=aviso)


if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)