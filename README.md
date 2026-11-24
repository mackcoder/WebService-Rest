<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,50:1e3a8a,100:38bdf8&height=200&section=header&text=%F0%9F%8C%90%20Web%20Services%20REST&fontSize=46&fontColor=ffffff&animation=fadeIn&fontAlignY=36&desc=Flask%20%2B%20Node.js%20conversando%20por%20HTTP%20%2B%20JSON&descAlignY=58&descSize=18" alt="Web Services REST" width="100%"/>

<img src="docs/typing.svg" alt="Destaques do laboratório" width="720"/>

<br/>

<!-- Status do repositório -->
<a href="https://github.com/mackcoder/LAB-COMP-Distribuida3/stargazers"><img src="https://img.shields.io/github/stars/mackcoder/LAB-COMP-Distribuida3?style=for-the-badge&logo=github&color=facc15&labelColor=0f172a" alt="Stars"/></a>
<a href="https://github.com/mackcoder/LAB-COMP-Distribuida3/watchers"><img src="https://img.shields.io/github/watchers/mackcoder/LAB-COMP-Distribuida3?style=for-the-badge&logo=github&color=38bdf8&labelColor=0f172a" alt="Watchers"/></a>
<a href="https://github.com/mackcoder/LAB-COMP-Distribuida3/network/members"><img src="https://img.shields.io/github/forks/mackcoder/LAB-COMP-Distribuida3?style=for-the-badge&logo=github&color=a78bfa&labelColor=0f172a" alt="Forks"/></a>
<img src="https://hits.sh/github.com/mackcoder/LAB-COMP-Distribuida3.svg?style=for-the-badge&label=visitas&color=4ade80&labelColor=0f172a" alt="Visitas"/>

<br/>

<img src="https://img.shields.io/github/last-commit/mackcoder/LAB-COMP-Distribuida3?style=flat-square&color=38bdf8&label=%C3%BAltimo%20commit" alt="Último commit"/>
<img src="https://img.shields.io/github/repo-size/mackcoder/LAB-COMP-Distribuida3?style=flat-square&color=a78bfa&label=tamanho" alt="Tamanho"/>
<img src="https://img.shields.io/github/languages/count/mackcoder/LAB-COMP-Distribuida3?style=flat-square&color=f472b6&label=linguagens" alt="Linguagens"/>
<img src="https://img.shields.io/badge/testes-7%2F7%20aprovados-4ade80?style=flat-square" alt="Testes"/>

<br/><br/>

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js"/>
<img src="https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=express&logoColor=white" alt="Express"/>
<img src="https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white" alt="JSON"/>
<img src="https://img.shields.io/badge/Codespaces-181717?style=for-the-badge&logo=github&logoColor=white" alt="Codespaces"/>

<br/><br/>

**🎓 Laboratório de Web Services · Computação Distribuída · Profs. Alcides e Mário**

Dois serviços REST independentes, um em **🐍 Python (Flask)** e outro em **🟩 Node.js (Express)**,<br/>
que conversam entre si e com clientes Python **apenas por HTTP + JSON**.

[🏗️ Arquitetura](#arquitetura) •
[🔌 Endpoints](#endpoints) •
[🧪 Exercícios](#exercicios) •
[🚀 Como executar](#como-executar) •
[✅ Testes](#testes) •
[🧠 Conceitos](#conceitos)

</div>

<p align="center">
  <img src="docs/teste-entrega.gif" alt="Execução dos testes da entrega" width="820">
</p>

---

<a id="arquitetura"></a>

## 🏗️ Arquitetura

<p align="center">
  <img src="docs/arquitetura.svg" alt="Arquitetura animada: cliente, Flask e Node" width="860">
</p>

> 💡 Cada serviço é **dono de uma parte dos dados**: nenhum deles tem sozinho a informação completa de um produto.

| | Serviço | Porta | Arquivo | Responsabilidade | Dados |
|:---:|---|:---:|---|---|---|
| 🐍 | **Flask** | `5000` | `aula-flask/app.py` | Serviço **fiscal** | `preco`, `categoria`, cálculo de imposto |
| 🟩 | **Node.js** | `3000` | `aula-node/server.js` | Serviço de **estoque** e porta de entrada | `nome`, `estoque`, proxy para o Flask |

```mermaid
flowchart LR
    C["🧑‍💻 Cliente Python"]
    N["🟩 Node.js :3000<br/>estoque + gateway"]
    F["🐍 Flask :5000<br/>serviço fiscal"]
    DN[("📦 nome, estoque")]
    DF[("💰 preco, categoria")]

    C -- "HTTP + JSON" --> N
    C -- "HTTP + JSON" --> F
    N -- "fetch (server-to-server)" --> F
    N --- DN
    F --- DF
```

> ⚠️ Os dados ficam **em memória** (dicionários/objetos): reiniciar um servidor volta ao estado inicial.

---

## 📁 Estrutura

```text
WebService/
├── 🐍 aula-flask/
│   └── app.py                # Flask: serviço fiscal (porta 5000)
├── 🟩 aula-node/
│   ├── index.js              # exemplo da aula (porta 3000)
│   ├── server.js             # Node: serviço de estoque + exercícios (porta 3000)
│   └── package.json
├── 📄 cliente.py             # exemplo da aula: consome os dois /api/data
├── 📊 cliente_relatorio.py   # Ex. 1 (relatório integrado) e Ex. 3 (monitor de status)
└── ✅ teste-deliver.py       # testes da entrega, sem pytest
```

---

<a id="endpoints"></a>

## 🔌 Endpoints

| Método | Rota | Serviço | Ex. | Descrição |
|:---:|---|:---:|:---:|---|
| ![GET](https://img.shields.io/badge/GET-38bdf8?style=flat-square) | `/api/data` | 🐍 🟩 | Aula | Mensagem de exemplo |
| ![GET](https://img.shields.io/badge/GET-38bdf8?style=flat-square) | `/detalhes/<id>` | 🐍 | 1, 2 | Preço e categoria do produto |
| ![GET](https://img.shields.io/badge/GET-38bdf8?style=flat-square) | `/estoque/:id` | 🟩 | 1, 5 | Nome e quantidade em estoque |
| ![GET](https://img.shields.io/badge/GET-38bdf8?style=flat-square) | `/api/full-info/:id` | 🟩 | 2 | **Proxy:** o Node consulta o Flask e devolve tudo junto |
| ![GET](https://img.shields.io/badge/GET-38bdf8?style=flat-square) | `/status` | 🐍 🟩 | 3 | Contrato idêntico: `{service, status, timestamp}` |
| ![POST](https://img.shields.io/badge/POST-4ade80?style=flat-square) | `/cadastrar` | 🟩 | 4A | Recebe o produto completo e distribui |
| ![POST](https://img.shields.io/badge/POST-4ade80?style=flat-square) | `/fiscal/cadastrar` | 🐍 | 4B | Aplica 20% de imposto e salva |

**Códigos HTTP usados:**

![200](https://img.shields.io/badge/200-OK-4ade80?style=flat-square)
![201](https://img.shields.io/badge/201-Criado-22c55e?style=flat-square)
![400](https://img.shields.io/badge/400-Entrada%20inv%C3%A1lida-f59e0b?style=flat-square)
![404](https://img.shields.io/badge/404-N%C3%A3o%20encontrado-f97316?style=flat-square)
![502](https://img.shields.io/badge/502-Servi%C3%A7o%20de%20tr%C3%A1s%20indispon%C3%ADvel-ef4444?style=flat-square)

---

<a id="exercicios"></a>

## 🧪 Exercícios

<details open>
<summary><b>1️⃣ Ex. 1 · Cliente integrador</b> <i>(integração no cliente)</i></summary>

<br/>

`cliente_relatorio.py` pede um ID, faz **um GET em cada servidor** e **funde** os dois JSONs. A integração acontece **no cliente**.

```mermaid
sequenceDiagram
    autonumber
    participant C as 🧑‍💻 Cliente
    participant N as 🟩 Node :3000
    participant F as 🐍 Flask :5000
    C->>N: GET /estoque/1
    N-->>C: {nome, estoque}
    C->>F: GET /detalhes/1
    F-->>C: {preco, categoria}
    Note over C: funde os dois JSONs
```

```text
Digite o ID do produto: 1
ID: 1 | Nome: Dell XPS 13 | Preço: R$ 2500.0 | Estoque: 10
```

</details>

<details open>
<summary><b>2️⃣ Ex. 2 · Comunicação server-to-server (proxy)</b> <i>(integração no servidor)</i></summary>

<br/>

<p align="center">
  <img src="docs/ex2-proxy.svg" alt="Animação do proxy: cliente → Node → Flask" width="860">
</p>

Em `GET /api/full-info/:id`, o **Node age como cliente do Flask** (`fetch`) e devolve o objeto completo. O cliente final só conhece o Node, e o Flask fica "escondido" atrás dele (padrão **API Gateway**). A integração acontece **no servidor**.

```json
GET http://localhost:3000/api/full-info/1
{"id":"1","nome":"Dell XPS 13","estoque":10,"categoria":"Laptops","preco":2500}
```

| | 1️⃣ Integração no cliente | 2️⃣ Integração no servidor |
|---|---|---|
| Quem chama os dois serviços | o cliente | o Node |
| O cliente conhece o Flask? | ✅ sim | ❌ não |
| Requisições do cliente | 2 | 1 |

</details>

<details open>
<summary><b>3️⃣ Ex. 3 · Padronização de contrato</b></summary>

<br/>

Os dois serviços expõem `GET /status` com **a mesma estrutura**, inclusive o formato do timestamp:

```json
{"service": "flask-fiscal", "status": "online", "timestamp": "2026-11-04T11:54:41.663Z"}
```

> 📜 A função `verificar_status(urls)` monitora qualquer lista de URLs **sem nenhum `if` por linguagem**: ela depende só do contrato.

</details>

<details open>
<summary><b>4️⃣ Ex. 4 · Cadastro com persistência distribuída</b></summary>

<br/>

<p align="center">
  <img src="docs/ex4-cadastro.svg" alt="Sequência animada do cadastro distribuído" width="860">
</p>

1. 🔠 O Node recebe o produto e converte o nome para **CAIXA ALTA**.
2. 📤 Envia ao Flask **só** os dados fiscais (`id`, `preco_base`, `categoria`).
3. 💰 O Flask aplica **+20%** (200.0 → **240.0**), salva em `produtos_tecnicos` e responde **201**.
4. 💾 **Só depois do 201** o Node salva `nome` e `estoque` em `produtos_comerciais`.

```mermaid
sequenceDiagram
    autonumber
    participant C as 🧑‍💻 Cliente
    participant N as 🟩 Node :3000
    participant F as 🐍 Flask :5000
    C->>N: POST /cadastrar {nome, preco_base, categoria, estoque}
    Note over N: nome → CAIXA ALTA
    N->>F: POST /fiscal/cadastrar {id, preco_base, categoria}
    Note over F: preco = preco_base × 1.20
    alt Flask respondeu 201
        F-->>N: 201 Created
        Note over N: salva nome + estoque
        N-->>C: 201 Created
    else Flask recusou ou caiu
        F--xN: erro / sem resposta
        N-->>C: 502 (nada é gravado)
    end
```

> 🛡️ Se o Flask recusar ou estiver fora do ar, o Node **não grava nada**, o que evita dados inconsistentes entre os serviços.

</details>

<details open>
<summary><b>5️⃣ Ex. 5 · Protocolo de erro e validação</b></summary>

<br/>

<p align="center">
  <img src="docs/ex5-validacao.svg" alt="Animação da validação do ID" width="860">
</p>

Os dois servidores validam o ID **antes** de processar. Um ID negativo ou não numérico interrompe a requisição com **400** e o mesmo corpo nos dois lados:

```json
GET http://localhost:3000/estoque/-5   →  400
{"error": "INVALID_ID", "message": "O ID deve ser um inteiro positivo"}
```

</details>

---

<a id="como-executar"></a>

## 🚀 Como executar

### 📋 Pré-requisitos

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nodejs npm -y
```

> ⚠️ O Node precisa ser **18 ou mais novo** (o `fetch` nativo é usado no proxy). Confira com `node -v`.

<table>
<tr>
<th>🐍 Terminal 1 · Flask</th>
<th>🟩 Terminal 2 · Node</th>
<th>🧑‍💻 Terminal 3 · Cliente e testes</th>
</tr>
<tr>
<td>

```bash
cd WebService/aula-flask
python3 -m venv venv
source venv/bin/activate
pip install Flask requests
python3 app.py
```

</td>
<td>

```bash
cd WebService/aula-node
npm install
node server.js
```

</td>
<td>

```bash
cd WebService
source aula-flask/venv/bin/activate
python3 cliente_relatorio.py
python3 teste-deliver.py
```

</td>
</tr>
</table>

### 🌍 No navegador (Codespaces)

Na aba **Ports**, abra a URL da porta `3000` ou `5000` e acrescente a rota no fim, por exemplo:

```text
https://<seu-codespace>-3000.app.github.dev/api/full-info/1
```

---

<a id="testes"></a>

## ✅ Testes da entrega

`teste-deliver.py` usa só `assert`, **sem pytest**, com **uma função por item** do enunciado:

| | Função | Verifica |
|:---:|---|---|
| ✅ | `exemplos_aula` | `/api/data` dos dois servidores |
| ✅ | `teste_preparacao_bases` | Bases iniciais `produtos_fiscais` e `produtos_estoque` |
| ✅ | `teste_ex1_cliente_integrador` | Linha do relatório idêntica à do enunciado |
| ✅ | `teste_ex2_proxy` | `/api/full-info/1` traz `nome` **e** `preco` |
| ✅ | `teste_ex3_status_padronizado` | Chaves `service`, `status` e `timestamp` nos dois `/status` |
| ✅ | `teste_ex4_cadastro_distribuido` | Node guarda `TECLADO` e Flask guarda o preço `240.0` |
| ✅ | `teste_ex5_validacao_id` | `-5` e `abc` retornam 400 com o JSON de erro padrão |

<div align="center">

### 🏆 Resultado: **7/7 testes aprovados**

![Progresso](https://img.shields.io/badge/progresso-100%25-4ade80?style=for-the-badge&labelColor=0f172a)

</div>

---

<a id="conceitos"></a>

## 🧠 Conceitos praticados

| | Conceito | Onde aparece |
|:---:|---|---|
| 🌐 | **REST:** recursos identificados por URI e métodos HTTP com significado (`GET` lê, `POST` cria) | todos os endpoints |
| 🔁 | **Stateless:** cada requisição carrega tudo o que precisa | todos os endpoints |
| 🤝 | **Interoperabilidade:** Python e JavaScript se comunicam só por HTTP + JSON | Ex. 1, 2, 4 |
| 🔀 | **Integração no cliente × no servidor** | Ex. 1 × Ex. 2 |
| 📜 | **Contratos de API:** formato de status e de erro iguais, independentes da linguagem | Ex. 3, 5 |
| 🧩 | **Responsabilidade por serviço e consistência distribuída** | Ex. 4 |

---

## 🛠️ Tecnologias

<div align="center">

<img src="https://skillicons.dev/icons?i=python,flask,nodejs,express,github,vscode,linux&theme=dark" alt="Tecnologias"/>

**Python 3 · Flask · requests · Node.js · Express · GitHub Codespaces**

</div>

---

<div align="center">

Feito com ☕ por **[Naoto Ushizaki](https://github.com/mackcoder)** · Computação Distribuída

⭐ Se este laboratório te ajudou, deixe uma estrela!

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:38bdf8,50:1e3a8a,100:0f172a&height=110&section=footer" alt="footer" width="100%"/>

</div>
