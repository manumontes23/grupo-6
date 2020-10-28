from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from datetime import date
from datetime import datetime

app = Flask(__name__)
""" entre los // y los : es el usuario """
""" entre : y el @ es la contraseña """
""" entre @ y / es el host o dominio """
""" el resto asi bien vergas es el nombre de la base de datos """
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b8a58880bd5f0e:e8b40148@us-cdbr-east-02.cleardb.com/heroku_adffbf225414c15'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return "<h1>Bienvenido</h1>"


""" Modelo de la bd """


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "usuario: " + str(self.username) + " Correo: " + str(self.email)


class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    apellidos = db.Column(db.String(45), unique=True, nullable=False)
    telefono = db.Column(db.String(45), unique=True, nullable=False)
    celular = db.Column(db.String(45), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return 'id: ' + str(self.id) + 'nombre: ' + str(self.nombre) + ' apellidos: ' + str(self.apellidos) + ' telefono: ' + str(self.telefono) + ' celular: ' + str(self.celular)+' email: ' + str(self.email)


class Riesgos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45), unique=True, nullable=False)
    fecha = db.Column(db.String(45), unique=True, nullable=False)
    valor = db.Column(db.Float(80), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey(
        'clientes.id'), nullable=False)

    def __repr__(self):
        return ' nombre: ' + str(self.nombre) + ' fecha: ' + str(self.fecha) + ' valor: ' + str(self.valor) + ' cliente_id: ' + str(self.cliente_id)

    """ Ejemplos """


@ app.route('/ejemplo', methods=['POST'])
def insertar():
    username = request.json['username']
    email = request.json['email']
    me = User(username=username, email=email)
    db.session.add(me)
    db.session.commit()
    if(me.id):
        return jsonify({'message': 'Registrado'})
    else:
        return jsonify({'message': 'Error'})


@ app.route('/ejemplo/<string:id>', methods=['DELETE'])
def eliminar(id):
    db.session.delete(id)
    db.session.commit()
    return jsonify({'message': 'Elimado'})


@ app.route('/ejemplo', methods=['GET'])
def obtenerTodos():
    usuarios = User.query.all()
    return jsonify({"message": "Resultados Extraidos con exito", "Usuarios": str(usuarios)
                    })


""" Rutas Jessica Parra """

""" Get """
""" Retorna los clientes del Riesgo de Mercado """


@ app.route('riesgoMercado/clientes/<string:nombre>', methods=['GET'])
def obtenerClientes():
    clientes = Riesgos.query.all()
    return jsonify({"message": "Clientes de Riesgo de Mercado", "Clientes": str(clientes)})


""" Post """
""" Crea un nuevo cliente para el riesgo de mercado """


@ app.route('riesgoMercado/clientes', methods=['POST'])
def crearClienteRM():
    id = request.json['id']
    nombre = request.json['nombre']
    apellidos = request.json['apellidos']
    telefono = request.json['telefono']
    celular = request.json['celular']
    email = request.json['email']
    me = Clientes(id=id, nombre=nombre, apellidos=apellidos,
                  telefono=telefono, celular=celular, email=email)
    db.session.add(me)
    db.session.commit()
    if(me.id):
        return jsonify({'message': 'Cliente registrado'})
    else:
        return jsonify({'message': 'Error en el registro'})


""" Put """
""" Actualiza un cliente del Riesgo de Mercado """
"@app.route('riesgoMercado/clientes/<string:nombre>', methods=['PUT'])"

""" Delete """
""" Elimina un cliente del Riesgo de Mercado """


@ app.route('riesgoMercado/clientes/<string:nombre>', methods=['DELETE'])
def eliminarCliente(id):
    db.session.delete(id)
    db.session.commit()
    return jsonify({'message': 'Eliminado el cliente'})


""" Get """
""" Retorna un cliente especifico del Riesgo de Mercado """


@ app.route('riesgoMercado/clientes/<string:nombre>', methods=['GET'])
def obtenerClienteEspecifico():
    cliente = Riesgos.query.filter_by(Riesgos.cliente_id).first()
    return jsonify({"message": "Cliente de Riesgo de Mercado", "Cliente": str(cliente)})


""" Put """
""" Actualiza un cliente especifico del Riesgo de Mercado """


@ app.route('riesgoMercado/clientes/<string:nombre>', methods=['PUT'])
def actualizarCliente(id):
    clienteA = update(Clientes).where(Clientes.id == id).values()
    return jsonify({"message": "Cliente actualizado", "Cliente": str(clienteA)})


""" Delete """
""" Elimina un cliente especifico del Riesgo de Mercado """


@ app.route('riesgoMercado/clientes/<string:nombre>', methods=['DELETE'])
def eliminarClienteEspecifico():
    cliente = Riesgos.query.filter_by(Riesgos.cliente_id).first()
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente eliminado'})


#########################################################################################################
""" RUTAS SANTIAGO JIMENEZ RAIGOSA """
#########################################################################################################

""" GET """
""" Retorna los clientes del VaR """

@ app.route('/var/clientes/', methods=['GET'])
def getClientesVar():
    #Encontramos los ids de los clientes que tienen como riesgo el var
    Clientes_var = Riesgos.query.filter_by(Riesgos.nombre == "VAR").all()
    return jsonify(Clientes_var)


""" Retorna un cliente especifico que tenga el valor en riesgo (cifras negativas)"""

@ app.route('/var/clienteID/<string:id>', methods=['GET'])
def getClientesVarID(id_buscar):
    #Encontramos el id que cumpla con las condiciones
    id_cliente = Riesgos.query.filter(Riesgos.id == id_buscar ,Riesgos.nombre=="VAR", Riesgos.valor <= 0).first()
    #Buscamos los datos de ese id
    datos_cliente = Clientes.query.filter(id_cliente.id)
    #entregamos los datos
    return jsonify(datos_cliente)
    

""" POST """
""" Crea un nuevo cliente para el VaR """


@ app.route('/var/crearCliente', methods=['POST'])
def crearClienteVar():
    # Datos cliente
    id_cliente = request.json['id']
    nombre = request.json['nombre']
    apellidos = request.json['apellidos']
    telefono = request.json['telefono']
    celular = request.json['celular']
    email = request.json['email']
    # Datos del varo
    nombre = "VAR"
    fecha = datetime.now()
    valor = request.json['valor']
    # Insertando los datos
    cliente = Clientes(id=id_cliente, nombre=nombre, apellidos=apellidos,
                       telefono=telefono, celular=celular, email=email)

    riesgo = Riesgos(nombre=nombre, fecha=fecha,
                     valor=valor, cliente_id=id_cliente)
    #Agregandolos
    db.session.add(cliente)
    db.session.add(riesgo)
    #Guardandolos
    db.session.commit()
    #Validando
    if(riesgo.id):
        return jsonify({'message': 'Registrado'})
    else:
        return jsonify({'message': 'Error'})


""" PUT """

""" Actualiza un cliente especifico para el VaR """

""" DELETE """

""" Borra un cliente especifico para el VaR """


@ app.route('/var/eliminarCliente/<string:id>', methods=['DELETE'])
def eliminarClienteVar(id_cliente):
    #Obtenemos cliente por id y que sea var
    cliente = Riesgos.query.filter_by(Riesgos.cliente_id == id_cliente, Riesgos.nombre == "VAR")
    #Eliminamos
    db.session.delete(cliente)
    #hacemos commit
    db.session.commit()
    #
    return jsonify({'message': 'Elimado'})


#########################################################################################################
""" RUTAS DANIEL LOPEZ RODRIGUEZ """
#########################################################################################################


""" GET """
"""" Retorna todos los riesgos """


@ app.route('/var', methods=['GET'])
def obtenerTodosRiesgos():
    riesgos = Riesgos.query.all()
    return jsonify({"message": "Resultados Extraidos con exito", "Riesgos": str(riesgos)
                    })


""" POST """
"""" Crea un registro con el valor del VaR """


@ app.route('/var', methods=['POST'])
def insertarRiesgo():
    nombre = request.json['nombre']
    fecha = request.json['fecha']
    valor = request.json['valor']
    cliente_id = request.json['cliente_id']
    me = Riesgos(nombre=nombre, fecha=fecha,
                 valor=valor, cliente_id=cliente_id)
    db.session.add(me)
    db.session.commit()
    if(me.id):
        return jsonify({'message': 'Registrado'})
    else:
        return jsonify({'message': 'Error'})


""" PUT """
"""" Actualiza el valor del VaR """


""" GET """
"""" Retorna el VaR en un periodo de tiempo t """


@ app.route('/var/<string:fecha>', methods=['GET'])
def consultarRiesgoPorFecha(fecha):
    riesgo = Riesgos.query.filter_by(fecha=fecha).first_or_404()
    return jsonify({"message": "Resultados Extraidos con exito", "Riesgo": str(riesgo)})


""" PUT """
"""" Actualizar el valor del VaR a un periodo de tiempo t """

""" DELETE """
"""" Borra el valor del VaR en un periodo de tiempo t """


@ app.route('/var/<string:fecha>', methods=['DELETE'])
def eliminarRiesgoPorFecha(fecha):
    riesgo = Riesgos.query.filter_by(fecha=fecha).first_or_404()
    db.session.delete(riesgo)
    db.session.commit()
    return jsonify({'message': 'Elimado'})


if __name__ == "_main_":
    app.run(debug=True, port=4000)
