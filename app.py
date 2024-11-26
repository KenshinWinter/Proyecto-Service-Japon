
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

# Definición de clases
class Cliente:
    def __init__(self, nombre, apellido, email, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono

class ServicioAd:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

class Reservacion:
    def __init__(self, cliente, fecha_inicio, fecha_fin, servicio):
        self.cliente = cliente
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.servicio = servicio

# Inicialización de la app Flask
app = Flask(__name__)

# Variables globales
clientes = []
servicios_adicionales = []
reservaciones = []
fechas_no_disponibles = [
    datetime(2024, 5, 15),
    datetime(2024, 5, 16),
    datetime(2024, 6, 1),
    datetime(2024, 6, 2),
    datetime(2024, 7, 10),
    datetime(2024, 7, 11)
]

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['GET', 'POST'])
def gestion_clientes():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        clientes.append(Cliente(nombre, apellido, email, telefono))
        return redirect(url_for('gestion_clientes'))
    return render_template('clientes.html', clientes=clientes)
    
@app.route('/clientes/eliminar/<int:cliente_id>', methods=['POST'])
def eliminar_cliente(cliente_id):
    if 0 <= cliente_id < len(clientes):
        del clientes[cliente_id]
    return redirect(url_for('gestion_clientes'))

@app.route('/servicios', methods=['GET', 'POST'])
def gestion_servicios():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        servicios_adicionales.append(ServicioAd(nombre, precio))
        return redirect(url_for('gestion_servicios'))
    return render_template('servicios.html', servicios=servicios_adicionales)
    
@app.route('/servicios/eliminar/<int:servicio_id>', methods=['POST'])
def eliminar_servicio(servicio_id):
    if 0 <= servicio_id < len(servicios_adicionales):
        del servicios_adicionales[servicio_id]
    return redirect(url_for('gestion_servicios'))

@app.route('/reservaciones', methods=['GET', 'POST'])
def gestion_reservaciones():
    if request.method == 'POST':
        cliente_id = int(request.form['cliente'])
        servicio_id = int(request.form['servicio'])
        fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d')
        fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d')

        if fecha_inicio > fecha_fin:
            return "Error: La fecha de inicio no puede ser posterior a la fecha de fin.", 400

        cliente = clientes[cliente_id]
        servicio = servicios_adicionales[servicio_id]
        reservaciones.append(Reservacion(cliente, fecha_inicio, fecha_fin, servicio))
        return redirect(url_for('gestion_reservaciones'))

    return render_template('reservaciones.html', clientes=clientes, servicios=servicios_adicionales, reservaciones=reservaciones)

@app.route('/reservaciones/eliminar/<int:reservacion_id>', methods=['POST'])
def eliminar_reservacion(reservacion_id):
    if 0 <= reservacion_id < len(reservaciones):
        del reservaciones[reservacion_id]
    return redirect(url_for('gestion_reservaciones'))

@app.route('/fechas_no_disponibles')
def fechas_no_disponibles_view():
    return render_template('fechas_no_disponibles.html', fechas=fechas_no_disponibles)

@app.route('/fechas_no_disponibles/eliminar/<int:fecha_id>', methods=['POST'])
def eliminar_fecha_no_disponible(fecha_id):
    if 0 <= fecha_id < len(fechas_no_disponibles):
        del fechas_no_disponibles[fecha_id]
    return redirect(url_for('fechas_no_disponibles_view'))

# Iniciar la app
if __name__ == '__main__':
    app.run(debug=True)
