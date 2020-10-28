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
    nombre = db.Column(db.String(45), nullable=False)
    apellidos = db.Column(db.String(45), nullable=False)
    telefono = db.Column(db.String(45), nullable=False)
    celular = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return 'id: ' + str(self.id) + 'nombre: ' + str(self.nombre) + ' apellidos: ' + str(self.apellidos) + ' telefono: ' + str(self.telefono) + ' celular: ' + str(self.celular)+' email: ' + str(self.email)


class Riesgos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(45), nullable=False)
    fecha = db.Column(db.String(45), nullable=False)
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


@ app.route('/riesgoMercado/clientes/<string:nombre>', methods=['GET'])
def obtenerClientes():
    clientes = Riesgos.query.all()
    return jsonify({"message": "Clientes de Riesgo de Mercado", "Clientes": str(clientes)})


""" Post """
""" Crea un nuevo cliente para el riesgo de mercado """


@ app.route('/riesgoMercado/clientes', methods=['POST'])
def crearClienteRM():
    id_cliente = request.json['id']
    nombre = request.json['nombre']
    apellidos = request.json['apellidos']
    telefono = request.json['telefono']
    celular = request.json['celular']
    email = request.json['email']

    nombre = "Riesgo de Mercado"
    fecha = datetime.now()
    valor = request.json['valor']
    cliente = Clientes(id=id_cliente, nombre=nombre, apellidos=apellidos, telefono=telefono, celular=celular, 
                email=email)
    
    riesgo = Riesgos(nombre=nombre, fecha=fecha, valor=valor, cliente_id=id_cliente)
    db.session.add(cliente)
    db.session.add(riesgo)
    db.session.commit()
    if(cliente.id):
        return jsonify({'message': 'Cliente registrado', "Cliente": str(cliente), "riesgo": str(riesgo)})
    else:
        return jsonify({'message': 'Error en el registro'})


""" Put """
""" Actualiza un cliente del Riesgo de Mercado """
"@app.route('riesgoMercado/clientes/<string:nombre>', methods=['PUT'])"

""" Delete """
""" Elimina un cliente del Riesgo de Mercado """


@ app.route('/riesgoMercado/clientes/<string:nombre>', methods=['DELETE'])
def eliminarCliente(id):
    db.session.delete(id)
    db.session.commit()
    return jsonify({'message': 'Eliminado el cliente'})


""" Get """
""" Retorna un cliente especifico del Riesgo de Mercado """


@ app.route('/riesgoMercado/clientes/<string:nombre>', methods=['GET'])
def obtenerClienteEspecifico(id_Cliente):
    cliente = Riesgos.query.filter_by(Riesgos.cliente_id == id_Cliente, Riesgos.nombre == 'Riesgo de Mercado').first()
    return jsonify({"message": "Cliente de Riesgo de Mercado", "Cliente": str(cliente)})


""" Put """
""" Actualiza un cliente especifico del Riesgo de Mercado """


@ app.route('/riesgoMercado/clientes/<string:nombre>', methods=['PUT'])
def actualizarCliente(id_Cliente):
    clienteA = update(Clientes).where(Clientes.id == id_Cliente).values()
    return jsonify({"message": "Cliente actualizado", "Cliente": str(clienteA)})


""" Delete """
""" Elimina un cliente especifico del Riesgo de Mercado """


@ app.route('/riesgoMercado/clientes/<string:nombre>', methods=['DELETE'])
def eliminarClienteEspecifico(id_Cliente):
    cliente = Riesgos.query.filter_by(Riesgos.cliente_id == id_Cliente, Riesgos.nombre == 'Riesgo de Mercado').first()
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente eliminado'})




#########################################################################################################
""" RUTAS SANTIAGO JIMENEZ RAIGOSA """
#########################################################################################################

""" GET """
""" Retorna los clientes del VaR """

@ app.route('/var/buscarClientes/', methods=['GET'])
def getClientesVar():
    #Encontramos los ids de los clientes que tienen como riesgo el var y los busca en Clientes
    Clientes_var = Clientes.query.filter(Clientes.id == Riesgos.cliente_id, Riesgos.nombre == "VAR").all()
    #Retorna los clientes asi bien chidos
    if(Clientes_var):
        return jsonify({"message": "Resultados Extraidos con exito", "Clientes": str(Clientes_var)})
    else:
        return jsonify({'message': 'No existen clientes'})
    

""" Retorna un cliente especifico que tenga el valor en riesgo (cifras negativas)"""

@ app.route('/var/buscarClientesPorId/<id_buscar>', methods=['GET'])
def getClientesVarID(id_buscar):
    #Encontramos el id que cumpla con las condiciones
    datos_cliente = Clientes.query.filter(Clientes.id == id_buscar,Riesgos.cliente_id== id_buscar, Riesgos.nombre=="VAR", Riesgos.valor <= 0).first()
    #Buscamos los datos de ese id
    #entregamos los datos
    if(datos_cliente):
        return jsonify({"message": "Resultados Extraidos con exito", "Cliente con valor en riesgo": str(datos_cliente)})
    else:
        return jsonify({'message': 'No existe ese cliente o con las especificaciones de tener el valor en riesgo'})
    

""" POST """
""" Crea un nuevo cliente para el VaR """

@ app.route('/var/crearClientes', methods=['POST'])
def crearClienteVar():
    # Datos cliente
    id_cliente = request.json['id']
    nombre_cliente = request.json['nombre']
    apellidos = request.json['apellidos']
    telefono = request.json['telefono']
    celular = request.json['celular']
    email = request.json['email']
    # Datos del var
    nombre_riesgo = "VAR"
    fecha = datetime.now()
    valor = request.json['valor']
    # Insertando los datos
    cliente = Clientes(id=id_cliente, nombre=nombre_cliente, apellidos=apellidos,
                       telefono=telefono, celular=celular, email=email)

    riesgo = Riesgos(nombre=nombre_riesgo, fecha=fecha,
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


@ app.route('/var/eliminarClientesPorId/<string:id_cliente>', methods=['DELETE'])
def eliminarClienteVar(id_cliente):
    #Obtenemos cliente por id y que sea var
    cliente = Riesgos.query.filter(Riesgos.cliente_id == id_cliente, Riesgos.nombre == "VAR").first()
    #Eliminamos
    if(cliente):
        db.session.delete(cliente)
        #hacemos commit
        db.session.commit()
        return jsonify({'message': 'Eliminado'})
    else:
        return jsonify({'message': 'Ese id no corrospendo a ningun cliente con riesgo var'})



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
