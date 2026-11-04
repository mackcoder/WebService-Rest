const express = require('express');
const app = express();
const PORT = 3000;
const FLASK_URL = 'http://localhost:5000';

app.use(express.json());

// Base de estoque (Preparação)
const produtos_estoque = {
    "1": { "nome": "Dell XPS 13", "estoque": 10 },
    "2": { "nome": "Monitor LG 29", "estoque": 5 }
};

// Produtos cadastrados pelo Exercício 4
const produtos_comerciais = {};

// ---------- Exercício 5: validação de ID ----------
function idValido(id) {
    return /^\d+$/.test(String(id)) && Number(id) > 0;
}

function erroIdInvalido(res) {
    return res.status(400).json({
        "error": "INVALID_ID",
        "message": "O ID deve ser um inteiro positivo"
    });
}

function buscarProduto(id) {
    return produtos_estoque[id] || produtos_comerciais[id];
}

// ---------- Exemplo da aula ----------
app.get('/api/data', (req, res) => {
    res.json({
        "mensagem": "Olá do Node.js!",
        "status": "sucesso",
        "tecnologia": "JavaScript"
    });
});

// ---------- Exercício 1: detalhes de estoque ----------
app.get('/estoque/:id', (req, res) => {
    const { id } = req.params;
    if (!idValido(id)) return erroIdInvalido(res);

    const produto = buscarProduto(id);
    if (!produto) {
        return res.status(404).json({ "error": "NOT_FOUND", "message": `Produto ${id} não encontrado` });
    }
    res.json({ id, ...produto });
});

// ---------- Exercício 2: proxy server-to-server ----------
app.get('/api/full-info/:id', async (req, res) => {
    const { id } = req.params;
    if (!idValido(id)) return erroIdInvalido(res);

    const produto = buscarProduto(id);
    if (!produto) {
        return res.status(404).json({ "error": "NOT_FOUND", "message": `Produto ${id} não encontrado` });
    }

    try {
        // O Node age como cliente do Flask
        const resposta = await fetch(`${FLASK_URL}/detalhes/${id}`);
        const fiscal = await resposta.json();
        if (!resposta.ok) return res.status(resposta.status).json(fiscal);

        res.json({ id, ...produto, ...fiscal });
    } catch (erro) {
        res.status(502).json({ "error": "FLASK_UNAVAILABLE", "message": "Não foi possível consultar o serviço fiscal" });
    }
});

// ---------- Exercício 3: status padronizado ----------
app.get('/status', (req, res) => {
    res.json({
        "service": "node-estoque",
        "status": "online",
        "timestamp": new Date().toISOString()
    });
});

// ---------- Exercício 4A: cadastro distribuído ----------
app.post('/cadastrar', async (req, res) => {
    const { id, nome, estoque, preco_base, categoria } = req.body || {};
    if (!idValido(id)) return erroIdInvalido(res);
    if (typeof nome !== 'string' || estoque === undefined || preco_base === undefined || !categoria) {
        return res.status(400).json({ "error": "INVALID_DATA", "message": "Envie id, nome, estoque, preco_base e categoria" });
    }

    // 1. Tratamento: nome em CAIXA ALTA
    const nomeTratado = nome.toUpperCase();

    try {
        // 2. Sincronização com o Flask
        const resposta = await fetch(`${FLASK_URL}/fiscal/cadastrar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: String(id), preco_base, categoria })
        });
        const fiscal = await resposta.json();

        // 3. Só salva se o Flask confirmou com 201
        if (resposta.status !== 201) {
            return res.status(resposta.status).json(fiscal);
        }

        produtos_comerciais[String(id)] = { "nome": nomeTratado, "estoque": estoque };
        res.status(201).json({ id: String(id), ...produtos_comerciais[String(id)], ...fiscal });
    } catch (erro) {
        res.status(502).json({ "error": "FLASK_UNAVAILABLE", "message": "Não foi possível cadastrar no serviço fiscal" });
    }
});

app.listen(PORT, () => {
    console.log(`Servidor Node rodando na porta ${PORT}`);
});