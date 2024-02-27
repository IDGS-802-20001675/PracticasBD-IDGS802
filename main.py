from flask import Flask, request, render_template, flash
from flask_wtf.csrf import CSRFProtect
import forms
from config import DevelopmentConfig
from models import db, Alumnos, Maestros

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)


'''     
Rutas o decoradores
'''
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.route("/indexM", methods=["GET", "POST"])
def indexM():
    form_maestros = forms.UserForm3(request.form)
    
    if request.method == 'POST' and form_maestros.validate():
        maestro = Maestros(
            nombre=form_maestros.nombre.data,
            apaterno=form_maestros.apaterno.data,
            amaterno=form_maestros.amaterno.data,
            escolaridad=form_maestros.escolaridad.data,
            materias=form_maestros.materias.data,
            email=form_maestros.email.data
        )
        
        db.session.add(maestro)
        db.session.commit()
    return render_template("indexM.html", form=form_maestros)


@app.route("/ABC_CompletoM", methods=["GET", "POST"])
def ABCompletoM():
    maestros = Maestros.query.all()
    
    return render_template("ABC_CompletoMaestros.html", maestros=maestros)
   

@app.route("/index", methods=["GET", "POST"])
def index():
    form_alumnos = forms.FormularioAlumnos(request.form)
    
    if request.method == 'POST' and form_alumnos.validate():
        alumno = Alumnos(
            nombre=form_alumnos.nombre.data,
            apaterno=form_alumnos.apaterno.data,
            email=form_alumnos.email.data
        )
        
        db.session.add(alumno)
        db.session.commit()
    return render_template("index.html", form=form_alumnos)


@app.route("/ABC_Completo", methods=["GET", "POST"])
def ABCompleto():
    alumnos = Alumnos.query.all()
    
    return render_template("ABC_Completo.html", alumnos=alumnos)
   

@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    form_alumnos = forms.FormularioAlumnos(request.form)
    
    if request.method == 'POST' and form_alumnos.validate():
        nom = form_alumnos.nombre.data    
        email = form_alumnos.email.data    
        apaterno = form_alumnos.apaterno.data   
        mensaje = 'Bienvenido: {}'.format(nom)
        flash(mensaje)
        print("nombre: {}".format(nom)) 
        print("email: {}".format(email)) 
        print("Apellido paterno: {}".format(apaterno)) 
    return render_template("alumnos.html", form=form_alumnos)


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
