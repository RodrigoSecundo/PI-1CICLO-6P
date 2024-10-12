from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@localhost/supguard_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_jwt'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

# Criar as tabelas no banco de dados
with app.app_context():
    db.create_all()

# Rota para criar um novo usuário (CREATE)
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    hashed_password = generate_password_hash(dados['senha'], method='sha256')
    novo_usuario = Usuario(nome=dados['nome'], email=dados['email'], senha=hashed_password)
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

# Rota para listar todos os usuários (READ)
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    output = []
    for usuario in usuarios:
        usuario_dados = {'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email}
        output.append(usuario_dados)
    return jsonify({'usuarios': output})

# Rota para buscar um único usuário por ID (READ)
@app.route('/usuarios/<id>', methods=['GET'])
def obter_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    usuario_dados = {'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email}
    return jsonify(usuario_dados)

# Rota para atualizar os dados de um usuário (UPDATE)
@app.route('/usuarios/<id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    dados = request.get_json()
    usuario.nome = dados['nome']
    usuario.email = dados['email']
    if 'senha' in dados:
        usuario.senha = generate_password_hash(dados['senha'], method='sha256')
    db.session.commit()
    return jsonify({'message': 'Usuário atualizado com sucesso!'})

# Rota para deletar um usuário (DELETE)
@app.route('/usuarios/<id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário deletado com sucesso!'})

# Rota de login (autenticação)
@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    usuario = Usuario.query.filter_by(email=dados['email']).first()
    if not usuario or not check_password_hash(usuario.senha, dados['senha']):
        return jsonify({'message': 'Login ou senha incorretos!'}), 401

    access_token = create_access_token(identity={'id': usuario.id, 'nome': usuario.nome, 'email': usuario.email})
    return jsonify({'token': access_token})

if __name__ == '__main__':
    app.run(debug=True)
