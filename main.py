import json
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask('carros')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:senai%40134@127.0.0.1/bd_carro'

mybd = SQLAlchemy(app)

with app.app_context():
    mybd.create_all()

class Carros(mybd.Model):
    __tablename__ = 'tb_carros'
    id_carro = mybd.Column(mybd.Integer, primary_key=True)
    marca = mybd.Column(mybd.String(100))
    modelo = mybd.Column(mybd.String(100))
    valor = mybd.Column(mybd.Float)
    cor = mybd.Column(mybd.String(100))
    numero_vendas = mybd.Column(mybd.Float)
    ano = mybd.Column(mybd.String(4))

    def to_json(self):
        return {
            "id_carro": self.id_carro, 
            "marca": self.marca, 
            "modelo": self.modelo, 
            "valor": self.valor, 
            "cor": self.cor, 
            "numero_vendas": self.numero_vendas,
            "ano": self.ano
        }

@app.route("/carros", methods=["GET"])
def selecionar_carros():
    carros_objetos = Carros.query.all()
    carro_json = [carro.to_json() for carro in carros_objetos]

    return gera_response(200, "carros", carro_json)

@app.route("/carros/<id_carro>")
def seleciona_carro_id(id_carro):
    carro_objeto = Carros.query.filter_by(id_carro=id_carro).first()
    carro_json = carro_objeto.to_json()

    return gera_response(200, "carros", carro_json)

@app.route("/carros", methods=["POST"])
def criar_carro():
    body = request.get_json()
    try:
        carro = Carros(
            id_carro=body["id_carro"], 
            marca=body["marca"], 
            modelo=body["modelo"], 
            valor=body["valor"], 
            cor=body["cor"],  
            numero_vendas=body["numero_vendas"],  
            ano=body["ano"]
        )

        mybd.session.add(carro)
        mybd.session.commit()

        return gera_response(201, "carros", carro.to_json(), "Criado com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "carros", {}, "Erro ao cadastrar!")
    
@app.route("/carros/<id_carro>", methods=["PUT"])
def atualizar_carro(id_carro):
    carro_objeto = Carros.query.filter_by(id_carro=id_carro).first()
    body = request.get_json()

    try:
        if('marca' in body):
            carro_objeto.marca = body['marca']
        if('modelo' in body):
            carro_objeto.modelo = body['modelo']
        if('valor' in body):
            carro_objeto.valor = body['valor']
        if('cor' in body):
            carro_objeto.cor = body['cor']
        if('numero_vendas' in body):
            carro_objeto.numero_vendas = body['numero_vendas']
        if('ano' in body):
            carro_objeto.ano = body['ano']

        mybd.session.add(carro_objeto)
        mybd.session.commit()  

        return gera_response(201, "carros", carro_objeto.to_json(), "Alterado com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "carros", {}, f"Erro ao cadastrar! {e}")

@app.route("/carros/<id_carro>", methods=["DELETE"])
def deletar_carro(id_carro):
    carro_objeto = Carros.query.filter_by(id_carro=id_carro).first()
    body = request.get_json()
    try:
        mybd.session.delete(carro_objeto)
        mybd.session.commit()
        return gera_response(200, "carros", carro_objeto.to_json(), "Deletado com sucesso!")
    except Exception as e:
        print('Erro', e)
        return gera_response(400, "carros", {}, f"Erro ao cadastrar! {e}")  

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if mensagem:
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")

if __name__ == "__main__":
    app.run(port=5000, host='localhost', debug=True)
