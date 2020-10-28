from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update

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
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    apellidos = db.Column(db.String(80), unique=True, nullable=False)
    telefono = db.Column(db.String(80), unique=True, nullable=False)
    celular = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return 'nombre: ' + str(nombre) + ' apellidos: ' + str(apellidos) + ' telefono: ' + str(telefono) + ' telefono: ' + str(celular)+' celular: ' + str(nombre)+' email: ' + str(email)


class Riesgos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    fecha = db.Column(db.Date, unique=True, nullable=False)
    valor = db.Column(db.Double(80), unique=True, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('Clientes.id'),
                           nullable=False)

    def __repr__(self):
        return ' nombre: ' + str(nombre) + ' fecha: ' + str(fecha) + ' valor: ' + str(valor) + ' cliente_id: ' + str(cliente_id)

    """ Ejemplos """


@app.route('/ejemplo', methods=['POST'])
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


@app.route('/ejemplo/<string:id>', methods=['DELETE'])
def eliminar(id):
    db.session.delete(id)
    db.session.commit()
    return jsonify({'message': 'Elimado'})


@app.route('/ejemplo', methods=['GET'])
def obtenerTodos():
    usuarios = User.query.all()
    return jsonify({"message":"Resultados Extraidos con exito","Usuarios":str(usuarios)
    })

""" Rutas Jessica Parra """

""" Get """
""" Retorna los clientes del Riesgo de Mercado """
@app.route('riesgoMercado/clientes/<string:nombre>', methods=['GET'])
def obtenerClientes():
    clientes = Riesgos.query.all()
    return jsonify({"message": "Clientes de Riesgo de Mercado", "Clientes":str(clientes)})

""" Post """
""" Crea un nuevo cliente para el riesgo de mercado """
@app.route('riesgoMercado/clientes', methods=['POST'])
def crearClienteRM():
    id = request.json['id']
    nombre = request.json['nombre']
    apellidos = request.json['apellidos']
    telefono = request.json['telefono']
    celular = request.json['celular']
    email = request.json['email']
    me = Clientes(id = id, nombre = nombre, apellidos = apellidos,
              telefono = telefono, celular = celular, email = email)
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
@app.route('riesgoMercado/clientes/<string:nombre>', methods=['DELETE'])
def eliminarCliente(id):
    db.session.delete(id)
    db.session.commit()
    return jsonify({'message': 'Eliminado el cliente'})

""" Get """
""" Retorna un cliente especifico del Riesgo de Mercado """
@app.route('riesgoMercado/clientes/<string:nombre>', methods=['GET'])
def obtenerClienteEspecifico():
    cliente = Riesgos.query.filter_by(Riesgos.cliente_id).first()
    return jsonify({"message": "Cliente de Riesgo de Mercado", "Cliente":str(cliente)})

""" Put """
""" Actualiza un cliente especifico del Riesgo de Mercado """
@app.route('riesgoMercado/clientes/<string:nombre>', methods=['PUT'])
def actualizarCliente(id):
    clienteA = update(Clientes).where(Clientes.id==id).\
        values()
    return jsonify({"message": "Cliente actualizado", "Cliente":str(clienteA)})

""" Delete """
""" Elimina un cliente especifico del Riesgo de Mercado """
@app.route('riesgoMercado/clientes/<string:nombre>', methods=['DELETE'])
def eliminarClienteEspecifico():
    cliente = Riesgos.query.filter_by(Riesgos.cliente_id).first()
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente eliminado'})


""" RUTAS SANTIAGO JIMENEZ RAIGOSA """

""" GET """
""" Retorna los clientes del VaR """

""" Retorna un cliente especifico que tenga el valor en riesgo (cifras negativas)"""

""" POST """
""" Crea un nuevo cliente para el VaR """


@app.route('/var/crearCliente', methods=['POST'])
def crearClienteVar():
    nombre = request.json['nombre']
    apellidos = request.json['apellidos']
    telefono = request.json['telefono']
    celular = request.json['celular']
    email = request.json['email']
    me = User(nombre = nombre, apellidos = apellidos,
              telefono = telefono, celular = celular, email = email)
    db.session.add(me)
    db.session.commit()
    if(me.id):
        return jsonify({'message': 'Registrado'})
    else:
        return jsonify({'message': 'Error'})


""" PUT """
""" Actualiza un cliente para el VaR """

""" Actualiza un cliente especifico para el VaR """

""" DELETE """
""" Borra un cliente para un VaR """

""" Borra un cliente especifico para el VaR """

""" RUTAS DANIEL LOPEZ RODRIGUEZ """

""" GET """
"""" Retorna todos los riesgos """
@app.route('/riesgos', methods=['GET'])
def obtenerTodosRiesgos():
    riesgos = Riesgos.query.all()
    return jsonify({"message":"Resultados Extraidos con exito","Riesgos":str(riesgos)          
    })

""" POST """
"""" Crea un registro con el valor del VaR """
@app.route('/riesgo', methods=['POST'])
def insertarRiesgo():
    nombre = request.json['nombre']
    fecha = request.json['fecha']
    valor = request.json['valor']
    cliente_id = request.json['cliente_id']   
    me = Riesgos(nombre=nombre, fecha=fecha, valor=valor, cliente_id=cliente_id)
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
@app.route('/riesgo/<string:fecha>', methods=['GET'])
def consultarRiesgoPorFecha(fecha):
    riesgo = Riesgos.query.filter_by(fecha=fecha).first_or_404()
    return jsonify({"message":"Resultados Extraidos con exito","Riesgo":str(riesgo)})


""" PUT """
"""" Actualizar el valor del VaR a un periodo de tiempo t """     

""" DELETE """
"""" Borra el valor del VaR en un periodo de tiempo t """ 
@app.route('/riesgo/<string:fecha>', methods=['DELETE'])
def eliminarRiesgoPorFecha(fecha):
    riesgo = Riesgos.query.filter_by(fecha=fecha).first_or_404()
    db.session.delete(riesgo)
    db.session.commit()
    return jsonify({'message': 'Elimado'}) 