from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de dados fiscais (Preparação)
produtos_fiscais = {
    "1": {"preco": 2500.0, "categoria": "Laptops"},
    "2": {"preco": 1200.0, "categoria": "Monitores"},
}

# Produtos cadastrados pelo Node (Exercício 4)
produtos_tecnicos = {}


# ---------- Exercício 5: validação de ID ----------
def id_invalido(id_produto):
    """Retorna a resposta 400 se o ID não for um inteiro positivo, senão None."""
    if not id_produto.isdigit() or int(id_produto) <= 0:
        return jsonify({
            "error": "INVALID_ID",
            "message": "O ID deve ser um inteiro positivo"
        }), 400
    return None


# ---------- Exemplo da aula ----------
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({
        "mensagem": "Olá do Flask!",
        "status": "sucesso",
        "tecnologia": "Python"
    })


# ---------- Exercícios 1 e 2: detalhes fiscais ----------
@app.route('/detalhes/<id_produto>', methods=['GET'])
def detalhes(id_produto):
    erro = id_invalido(id_produto)
    if erro:
        return erro

    produto = produtos_fiscais.get(id_produto) or produtos_tecnicos.get(id_produto)
    if produto is None:
        return jsonify({"error": "NOT_FOUND", "message": f"Produto {id_produto} não encontrado"}), 404

    return jsonify({"id": id_produto, **produto})


# ---------- Exercício 3: status padronizado ----------
@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "service": "flask-fiscal",
        "status": "online",
        "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    })


# ---------- Exercício 4B: cadastro fiscal ----------
@app.route('/fiscal/cadastrar', methods=['POST'])
def cadastrar_fiscal():
    dados = request.get_json(silent=True) or {}
    id_produto = str(dados.get("id", ""))

    erro = id_invalido(id_produto)
    if erro:
        return erro

    try:
        preco_base = float(dados["preco_base"])
        categoria = dados["categoria"]
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "INVALID_DATA", "message": "Envie preco_base (número) e categoria"}), 400

    # 1. Cálculo fiscal: 20% de imposto
    preco_calculado = round(preco_base * 1.20, 2)

    # 2. Persistência fiscal
    produtos_tecnicos[id_produto] = {"preco": preco_calculado, "categoria": categoria}

    # 3. Resposta 201
    return jsonify({"id": id_produto, **produtos_tecnicos[id_produto]}), 201


if __name__ == '__main__':
    # No Codespaces, use host='0.0.0.0' para permitir acesso externo
    app.run(debug=True, host='0.0.0.0', port=5000)