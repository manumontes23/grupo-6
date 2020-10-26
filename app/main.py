from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://b8a58880bd5f0e:e8b40148@us-cdbr-east-02.cleardb.com/heroku_adffbf225414c15?reconnect=true'
db = SQLAlchemy(app)


@app.route('/')
def index():
  return "<h1>Bienvenido</h1>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
@app.route('/ejemplo', methods=['POST'])
def insertar():
    username=request.json['username']
    email=request.json['email']
    me = User(username, email)
    db.session.add(me)
    db.session.commit()
    if(me.id):
        return jsonify({'message': 'Registrado'})
    else:
        return jsonify({'message': 'Error'})

@app.route('/ejemplo/<string:id>', methods=['DELETE'])
def eliminar(id):
    db.session.delete(me)
    db.session.commit()
    return jsonify({'message': 'Elimado'})

@app.route('/ejemplo', methods=['GET'])
def obtenerTodos():
    return jsonify(User.query.all())

