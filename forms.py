from wtforms import Form,validators
from wtforms import StringField,TextAreaField,SelectField,RadioField,IntegerField, BooleanField
from wtforms import EmailField, TelField, DateField


""" class UserForm(Form):
    nombre=StringField("nombre")
    email=EmailField("correo")
    apaterno=StringField("apaterno")
    materias=SelectField(choices=[('Español','esp'),('Matematicas','mat'), ('Ingles','ING') ])
    radios=RadioField('Curso',choices=[('1','1'),('2','2'),('3','3')]) """
 
class PizzaForm(Form):
    
      id=IntegerField('id')
      nombre=StringField("Nombre",[
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4,max=10,message="Ingresa un nombre vailido")
    ])
      direccion=StringField("Dirección",[
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4,max=10,message="Ingresa direccion vailida")
    ])
      telefono=StringField("Teléfono",[
        validators.DataRequired(message="El campo es requerido"),
    ])
      tamanio = RadioField("Tamaño", choices=[("Chica", "Chica $40"), 
                                              ("Mediana", "Mediana $80"),
                                              ("Grande","Grande $120")])
      jamon = BooleanField('Jamón $10')
      pinia = BooleanField('Piña $10')
      champiniones = BooleanField('Champiñones $10')
      
      numero=IntegerField("Número de Pizzas",[
        validators.DataRequired(message="El campo es requerido"),
    ])
      fecha = DateField("Fecha de Venta")

 
class UserForm4(Form):
    nombre = StringField("nombre")
    direccion = StringField("direccion")
    telefono = StringField("telefono")
    numPizza = IntegerField("numpizza")
    tamano = RadioField('Tamaño', choices=[('Chica', 'Chica'), ('Mediana', 'Mediana'), ('Grande', 'Grande')])
    jamon = BooleanField('Jamón')
    pina = BooleanField('Piña')
    champinones = BooleanField('Champiñones')

class UserForm(Form):
    nombre = StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=10, message='Ingrese un nombre válido')
    ])
    email = EmailField("correo", [
        validators.Email(message='Ingrese un correo válido')
    ])
    apaterno = StringField("apaterno")
    edad = IntegerField("edad", [
        validators.NumberRange(min=1, max=20, message='Ingrese un valor válido, debe estar entre 1 y 20')
    ])

class UserForm2(Form):
    id=IntegerField('id')
    nombre = StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=10, message='Ingrese un nombre válido')
    ])
    apaterno = StringField("apaterno")
    email = EmailField("correo", [
        validators.Email(message='Ingrese un correo válido')
    ])

class UserForm3(Form):
    id=IntegerField('id')
    nombre = StringField("nombre", [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4, max=10, message='Ingrese un nombre válido')
    ])
    apaterno = StringField("apaterno")
    amaterno = StringField("amaterno")
    escolaridad = StringField("escolaridad")
    materias = StringField("materias")
    
    email = EmailField("correo", [
        validators.Email(message='Ingrese un correo válido')
    
    ]) 

    """ materias=SelectField(choices=[('Español','esp'),('Matematicas','mat'), ('Ingles','ING') ])
    radios=RadioField('Curso',choices=[('1','1'),('2','2'),('3','3')]) """