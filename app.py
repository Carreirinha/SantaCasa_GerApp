from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/mydatabase"
mongo = PyMongo(app)

users_collection = mongo.db.users
clients_collection = mongo.db.clients

@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    data = request.form
    email = data.get('email')
    senha = data.get('senha')
    if email and senha:
        user_data = {'email': email, 'senha': senha}
        users_collection.insert_one(user_data)
        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 200
    else:
        return jsonify({'error': 'É necessário fornecer email e senha!'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('email')
    senha = data.get('senha')
    user = users_collection.find_one({'email': email, 'senha': senha})
    if user:
        return jsonify({'message': 'Login bem-sucedido!'}), 200
    else:
        return jsonify({'error': 'Credenciais inválidas'}), 401

@app.route('/cadastro_cliente', methods=['POST'])
def cadastrar_cliente():
    data = request.form
    identificador = data.get('identificador')
    nome = data.get('nome')
    data_nascimento = datetime.strptime(data.get('data_nascimento'), '%Y-%m-%d')
    sexo = data.get('sexo')
    observacoes = data.get('observacoes')
    imagem = request.files['imagem']
    data_cadastro = datetime.strptime(data.get('data_cadastro'), '%Y-%m-%d %H:%M:%S')
    if identificador and nome and data_nascimento and sexo and observacoes and imagem and data_cadastro:
        client_data = {
            'identificador': identificador,
            'nome': nome,
            'data_nascimento': data_nascimento,
            'sexo': sexo,
            'observacoes': observacoes,
            'imagem': imagem.read(),
            'data_cadastro': data_cadastro
        }
        clients_collection.insert_one(client_data)
        return jsonify({'message': 'Cliente cadastrado com sucesso!'}), 200
    else:
        return jsonify({'error': 'Todos os campos são obrigatórios!'}), 400

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = []
    for client in clients_collection.find():
        client['_id'] = str(client['_id'])
        clientes.append(client)
    return jsonify(clientes)

if __name__ == '__main__':
    app.run(debug=True)
