# LAB-COMP-Distribuida3 · Web Services REST

Laboratório de **Web Services** da disciplina **Computação Distribuída** (Profs. Alcides e Mário).
Dois serviços REST independentes, um em **Python (Flask)** e outro em **Node.js (Express)**, que conversam entre si e com clientes Python apenas por **HTTP + JSON**.

<p align="center">
  <img src="docs/teste-entrega.gif" alt="Execução dos testes da entrega" width="820">
</p>

---

## Arquitetura

<p align="center">
  <img src="docs/arquitetura.svg" alt="Arquitetura animada: cliente, Flask e Node" width="860">
</p>

Cada serviço é **dono de uma parte dos dados**: nenhum deles tem sozinho a informação completa de um produto.

| Serviço | Porta | Arquivo | Responsabilidade | Dados |
|---|---|---|---|---|
| **Flask** | 5000 | `aula-flask/app.py` | Serviço **fiscal** | `preco`, `categoria`, cálculo de imposto |
| **Node.js** | 3000 | `aula-node/server.js` | Serviço de **estoque** e porta de entrada | `nome`, `estoque`, proxy para o Flask |

Os dados ficam em memória (dicionários/objetos), e reiniciar um servidor volta ao estado inicial.

---

## Estrutura

```
WebService/
├── aula-flask/
│   └── app.py                # Flask: serviço fiscal (porta 5000)
├── aula-node/
│   ├── index.js              # exemplo da aula (porta 3000)
│   ├── server.js             # Node: serviço de estoque + exercícios (porta 3000)
│   └── package.json
├── cliente.py                # exemplo da aula: consome os dois /api/data
├── cliente_relatorio.py      # Ex. 1 (relatório integrado) e Ex. 3 (monitor de status)
└── teste-deliver.py          # testes da entrega, sem pytest
```

---

## Endpoints

| Método | Rota | Serviço | Exercício | Descrição |
|---|---|---|---|---|
| `GET` | `/api/data` | Flask e Node | Aula | Mensagem de exemplo |
| `GET` | `/detalhes/<id>` | Flask | 1, 2 | Preço e categoria do produto |
| `GET` | `/estoque/:id` | Node | 1, 5 | Nome e quantidade em estoque |
| `GET` | `/api/full-info/:id` | Node | 2 | **Proxy:** o Node consulta o Flask e devolve tudo junto |
| `GET` | `/status` | Flask e Node | 3 | Contrato idêntico: `{service, status, timestamp}` |
| `POST` | `/cadastrar` | Node | 4A | Recebe o produto completo e distribui |
| `POST` | `/fiscal/cadastrar` | Flask | 4B | Aplica 20% de imposto e salva |

Códigos HTTP usados: **200** OK · **201** criado · **400** entrada inválida · **404** não encontrado · **502** serviço de trás indisponível.

---

## Exercícios

### Ex. 1: Cliente integrador
`cliente_relatorio.py` pede um ID, faz **um GET em cada servidor** e **funde** os dois JSONs. A integração acontece **no cliente**.

```
Digite o ID do produto: 1
ID: 1 | Nome: Dell XPS 13 | Preço: R$ 2500.0 | Estoque: 10
```

### Ex. 2: Comunicação server-to-server (proxy)
Em `GET /api/full-info/:id`, o **Node age como cliente do Flask** (`fetch`) e devolve o objeto completo. O cliente final só conhece o Node, e o Flask fica "escondido" atrás dele (padrão **API Gateway**). A integração acontece **no servidor**.

```json
GET http://localhost:3000/api/full-info/1
{"id":"1","nome":"Dell XPS 13","estoque":10,"categoria":"Laptops","preco":2500}
```

### Ex. 3: Padronização de contrato
Os dois serviços expõem `GET /status` com **a mesma estrutura**, inclusive o formato do timestamp:

```json
{"service": "flask-fiscal", "status": "online", "timestamp": "2026-11-04T11:54:41.663Z"}
```

A função `verificar_status(urls)` monitora qualquer lista de URLs **sem nenhum `if` por linguagem**: ela depende só do contrato.

### Ex. 4: Cadastro com persistência distribuída

<p align="center">
  <img src="docs/ex4-cadastro.svg" alt="Sequência animada do cadastro distribuído" width="860">
</p>

1. O Node recebe o produto e converte o nome para **CAIXA ALTA**.
2. Envia ao Flask **só** os dados fiscais (`id`, `preco_base`, `categoria`).
3. O Flask aplica **+20%** (200.0 → **240.0**), salva em `produtos_tecnicos` e responde **201**.
4. **Só depois do 201** o Node salva `nome` e `estoque` em `produtos_comerciais`.

Se o Flask recusar ou estiver fora do ar, o Node não grava nada, o que evita dados inconsistentes entre os serviços.

### Ex. 5: Protocolo de erro e validação
Os dois servidores validam o ID **antes** de processar. Um ID negativo ou não numérico interrompe a requisição com **400** e o mesmo corpo nos dois lados:

```json
GET http://localhost:3000/estoque/-5   →  400
{"error": "INVALID_ID", "message": "O ID deve ser um inteiro positivo"}
```

---

## Como executar

### Pré-requisitos
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nodejs npm -y
```
O Node precisa ser **18 ou mais novo** (o `fetch` nativo é usado no proxy). Confira com `node -v`.

### 1. Flask (Terminal 1)
```bash
cd WebService/aula-flask
python3 -m venv venv
source venv/bin/activate
pip install Flask requests
python3 app.py
```

### 2. Node (Terminal 2)
```bash
cd WebService/aula-node
npm install
node server.js
```

### 3. Cliente e testes (Terminal 3)
```bash
cd WebService
source aula-flask/venv/bin/activate
python3 cliente_relatorio.py     # relatório integrado + status
python3 teste-deliver.py         # todos os testes da entrega
```

### No navegador (Codespaces)
Na aba **Ports**, abra a URL da porta 3000 ou 5000 e acrescente a rota no fim, por exemplo:
`https://<seu-codespace>-3000.app.github.dev/api/full-info/1`

---

## Testes da entrega

`teste-deliver.py` usa só `assert`, **sem pytest**, com **uma função por item** do enunciado:

| Função | Verifica |
|---|---|
| `exemplos_aula` | `/api/data` dos dois servidores |
| `teste_preparacao_bases` | Bases iniciais `produtos_fiscais` e `produtos_estoque` |
| `teste_ex1_cliente_integrador` | Linha do relatório idêntica à do enunciado |
| `teste_ex2_proxy` | `/api/full-info/1` traz `nome` **e** `preco` |
| `teste_ex3_status_padronizado` | Chaves `service`, `status` e `timestamp` nos dois `/status` |
| `teste_ex4_cadastro_distribuido` | Node guarda `TECLADO` e Flask guarda o preço `240.0` |
| `teste_ex5_validacao_id` | `-5` e `abc` retornam 400 com o JSON de erro padrão |

Resultado: **7/7 testes aprovados**.

---

## Conceitos praticados

- **REST:** recursos identificados por URI e métodos HTTP com significado (`GET` lê, `POST` cria).
- **Stateless:** cada requisição carrega tudo o que precisa.
- **Interoperabilidade:** Python e JavaScript se comunicam só por HTTP + JSON.
- **Integração no cliente x no servidor:** Ex. 1 x Ex. 2.
- **Contratos de API:** formato de status e de erro iguais, independentes da linguagem.
- **Responsabilidade por serviço e consistência distribuída:** Ex. 4.

## Tecnologias
Python 3 · Flask · requests · Node.js · Express · GitHub Codespaces
