from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

#Mensaje de bienvenida
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/bdpythonapy'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://maihuire@upc-demo-server:theonly-1@upc-demo-server.mysql.database.azure.com:3306/bdpythonapy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#creación de tabla categoria
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self, cat_nom,cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp

#Creacion de tabla usuario

class Usuario(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    nombreape = db.Column(db.String(100))
    tipodoc = db.Column(db.String(15))
    dni = db.Column(db.String(15))
    email = db.Column(db.String(50))
    perfil =  db.Column(db.String(25))
    username =  db.Column(db.String(15))
    clave = db.Column(db.String(20))
    
    def __init__(self, nombreape, tipodoc,dni,email,perfil,username,clave):
        self.nombreape = nombreape
        self.tipodoc = tipodoc
        self.dni = dni
        self.email = email
        self.perfil = perfil
        self.username = username
        self.clave = clave

db.create_all()

#Schema Categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp')

#Schema Usuario
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('userid', 'nombreape', 'tipodoc','dni','email','perfil','username','clave')

#Una sola respuesta
categoria_schema = CategoriaSchema()
usuario_schema=UsuarioSchema()

#Cuando sean muchas respuestas.
categorias_schema = CategoriaSchema(many=True)
usuarios_schema=UsuarioSchema(many=True)


#GET########################################
@app.route('/categoria', methods=['GET'])

def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

#GET por ID#################################
@app.route('/categoria/<id>', methods=['GET'])

def get_categoria_x_id(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)


#POST#################################
@app.route('/categoria', methods=['POST'])
def insert_categoria():
    data = request.get_json(force=True)
    cat_nom = data["cat_nom"]
    cat_desp = data["cat_desp"]

    nuevocategoria = Categoria(cat_nom, cat_desp)

    db.session.add(nuevocategoria)
    db.session.commit()
    return categoria_schema.jsonify(nuevocategoria)

#PUT#################################################
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    actualizarcategoria = Categoria.query.get(id)
    cat_nom = request.json['cat_nom']
    cat_desp = request.json['cat_desp']

    actualizarcategoria.cat_nom = cat_nom
    actualizarcategoria.cat_desp=cat_desp

    db.session.commit()
    return categoria_schema.jsonify(actualizarcategoria)


#Schema usuario

#POST

@app.route('/usuario', methods=['POST'])
def insert_user():
    data = request.get_json(force = True)
    nombreape= data["nombreape"]
    tipodoc= data["tipodoc"]
    dni= data["dni"]
    email= data["email"]
    perfil= data["perfil"]
    username= data["username"]
    clave= data["clave"]

    nuevousuario = Usuario(nombreape, tipodoc,dni,email,perfil,username,clave)

    db.session.add(nuevousuario)
    db.session.commit()
    return usuario_schema.jsonify(nuevousuario)

#GET
@app.route('/usuario', methods=['GET'])

def get_usuarios():
    all_usuarios = Usuario.query.all()
    result = usuarios_schema.dump(all_usuarios)
    return jsonify(result)


#Mensaje de bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({'': 'Bienvenido al tutorial API REST Python'})

if __name__=="__main__":
    app.run(debug=True)