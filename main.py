from flask import Flask, request, render_template, flash,  jsonify, redirect,url_for, Response
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import extract
import forms
import json,os
from datetime import datetime, date, timedelta
from config import DevelopmentConfig
from models import db, Alumnos, Maestros, Pizzas, Ventas
from calendar import monthrange
from datetime import datetime,timedelta

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

temporal = []
id_pizza = 1

'''     
Rutas o decoradores
'''
'''     
Práctica PIZZA
'''
def guardar_temporal_en_txt(temporal):
    with open("temporal.txt", "w") as file:
        for pedido in temporal:
            file.write(str(pedido) + "\n")

datoel=forms.PizzaForm()



@app.route("/pizza", methods=["GET", "POST"])
def pizzas():
    global temporal, id_pizza, datoel
    pizza_form = forms.PizzaForm(request.form)
    
    ventas = None 
    suma_total = None 
    mensaje=None
    
    if request.method == "POST" and not ("fecha_consulta" in request.form or "mes_consulta" in request.form or "dia_consulta" in request.form):
        ingredientes_seleccionados = []
        if pizza_form.jamon.data:
            ingredientes_seleccionados.append("Jamon")
        if pizza_form.pinia.data:
            ingredientes_seleccionados.append("Pinia")
        if pizza_form.champiniones.data:
            ingredientes_seleccionados.append("Champiniones")

        tamanio_seleccionado = pizza_form.tamanio.data
        if tamanio_seleccionado == 'Chica':
            tamanio_int = 40
        elif tamanio_seleccionado == 'Mediana':
            tamanio_int = 80
        else:
            tamanio_int = 120

        num_ingredientes = len(ingredientes_seleccionados) * 10
        total = int(num_ingredientes) + tamanio_int
        totalP = total * pizza_form.numero.data
        fecha_seleccionada=pizza_form.fecha.data
        dia_semana = fecha_seleccionada.strftime('%A')
        print(dia_semana)

        
        temporal.append({ 
            'id': id_pizza,
            'nombre': pizza_form.nombre.data,
            'direccion': pizza_form.direccion.data,
            'telefono': pizza_form.telefono.data,
            'tamanio': tamanio_seleccionado,
            'ingredientes': ingredientes_seleccionados,
            'numero': pizza_form.numero.data,
            'totalP': totalP,
            'fecha': pizza_form.fecha.data,
            'dia':dia_semana
        })
        guardar_temporal_en_txt(temporal)   
        datoel=pizza_form
        
        id_pizza += 1
    if request.method == "POST" or request.method == "GET" and "mes_consulta" not in request.form:
        fecha_consulta_str = request.form.get("fecha_consulta")
        if fecha_consulta_str:
            fecha_consulta = datetime.strptime(fecha_consulta_str, "%Y-%m-%d").date()
            
            ventas = Pizzas.query.filter(Pizzas.fecha >= fecha_consulta).filter(Pizzas.fecha < fecha_consulta + timedelta(days=1)).all()
            suma_total = sum(venta.total for venta in ventas)
            
    if request.method == "POST" or request.method == "GET" and "mes_consulta" in request.form:
        mes_consulta_str = request.form.get("mes_consulta")
        if mes_consulta_str:
            fecha_consulta = datetime.now().replace(month=int(mes_consulta_str))
            
            ventas = Pizzas.query.filter(extract('month', Pizzas.fecha) == int(mes_consulta_str)).all()
            suma_total = sum(venta.total for venta in ventas)
            
    if request.method == "POST" or request.method == "GET" and "dia_consulta" in request.form:
        dia_consulta = request.form.get("dia_consulta")
        if dia_consulta:
         ventas = Pizzas.query.filter(Pizzas.dia == dia_consulta).all()
         suma_total = sum(venta.total for venta in ventas)   
    
    return render_template("pizza.html", form=pizza_form, temporal=temporal, ventas=ventas,suma_total=suma_total,mensaje=mensaje)







@app.route("/confirmar", methods=["POST"])
def confirmar_registro():
    global temporal


    for registro in temporal:
        pizza = Pizzas(
            nombre=registro['nombre'],
            direccion=registro['direccion'],
            telefono=registro['telefono'],
            tamanio=registro['tamanio'],
            ingredientes=', '.join(registro['ingredientes']),  
            numero=registro['numero'],
            total=registro['totalP'],
            fecha=registro['fecha'],
            dia=registro['dia']
            
        )
    pizza.total = sum(registro['totalP'] for registro in temporal)
    print(pizza)
    
    db.session.add(pizza)

    db.session.commit()
    temporal = [] 
    mensaje="Venta exitosa"
    flash(mensaje)

    return redirect("/pizza")  

 
@app.route("/eliminarPizza", methods=["POST"])
def eliminar_registro():
    global temporal, datoel
    
    id_pizza = int(request.form["id"])
    temporal = [registro for registro in temporal if registro["id"] != id_pizza]
   # return redirect(url_for("/pizza", form=datoel))
    return render_template("pizza.html", form=datoel, temporal=temporal)



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
