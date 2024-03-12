from flask_sqlalchemy import SQLAlchemy
import datetime
db=SQLAlchemy()


class Pizzas(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    telefono=db.Column(db.String(50))
    tamanio=db.Column(db.String(50))
    ingredientes =db.Column(db.String(50))
    numero =db.Column(db.Integer)
    total =db.Column(db.Integer)
    fecha=db.Column(db.DateTime)
    dia=db.Column(db.String(50))

class Ventas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(50))
    direccion_cliente = db.Column(db.String(100))  # Asegúrate de que la longitud sea suficiente
    telefono_cliente = db.Column(db.String(20))
    total = db.Column(db.Float)
    fecha_pedido = db.Column(db.DateTime)
    dia_semana = db.Column(db.String(10))



class Alumnos(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    apaterno=db.Column(db.String(50))
    email=db.Column(db.String(50))
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)

class Maestros(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    apaterno=db.Column(db.String(50))
    amaterno=db.Column(db.String(50))
    escolaridad=db.Column(db.String(50))
    materias=db.Column(db.String(50))
    email=db.Column(db.String(50))
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)
    

