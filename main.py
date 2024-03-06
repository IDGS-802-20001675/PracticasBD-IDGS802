from flask import Flask, request, render_template, flash
from flask_wtf.csrf import CSRFProtect
import forms
from config import DevelopmentConfig
from models import db, Alumnos, Maestros, Pizzas

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

'''     
Rutas o decoradores
'''
'''     
Práctica PIZZA
'''
@app.route("/pizzas", methods=["GET", "POST"])
def pizzas():
    form_pizza = forms.UserForm4(request.form)
    
    if request.method == 'POST' and form_pizza.validate():
        tamano_pizza = form_pizza.tamano.data
        num_pizza = form_pizza.numPizza.data
        
        # Mapear los tamaños de pizza a valores numéricos
        tamanos = {'Chica': 1, 'Mediana': 2, 'Grande': 3}
        
        # Obtener el tamaño seleccionado del formulario
        tamano_numerico = tamanos.get(tamano_pizza, 0)
        
        # Calcular el costo base del tamaño de la pizza
        costo_base_por_tamano = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
        costo_base = costo_base_por_tamano.get(tamano_pizza, 0)
        
        # Calcular el costo de los ingredientes seleccionados
        costo_ingredientes = 0
        if 'jamon' in request.form:
            costo_ingredientes += 10
        if 'pina' in request.form:
            costo_ingredientes += 10
        if 'champinones' in request.form:
            costo_ingredientes += 10
        
        # Calcular el costo total de la pizza
        costo_total = (costo_base + costo_ingredientes) * num_pizza
        
        # Crear un objeto de pizza con la información recibida
        nueva_pizza = Pizzas(
            nombre=form_pizza.nombre.data,
            direccion=form_pizza.direccion.data,
            telefono=form_pizza.telefono.data,
            tamano=tamano_numerico,  # Asignar el valor numérico correspondiente
            costo=costo_total
        )
        
        # Agregar la nueva pizza a la sesión de la base de datos
        db.session.add(nueva_pizza)
        
        # Hacer commit para guardar los cambios en la base de datos
        db.session.commit()
        
        flash(f'Costo total del pedido: ${costo_total}')  # Mostrar el costo total al usuario
        
        # Redirigir a una página de confirmación o realizar otras acciones necesarias
        
    return render_template("pizzas.html", form=form_pizza)






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
