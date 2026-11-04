import requests
from cliente_relatorio import buscar_relatorio, formatar_relatorio, verificar_status

 
FLASK = "http://localhost:5000"
NODE = "http://localhost:3000"

def exemplos_aula():
    for url, tecnologia in [(f"{FLASK}/api/data", "Python"), (f"{NODE}/api/data", "JavaScript")]:
        dados = requests.get(url).json()
        assert dados["status"] == "sucesso" and dados["tecnologia"] == tecnologia
 
 
def teste_preparacao_bases():
    assert requests.get(f"{FLASK}/detalhes/1").json()["preco"] == 2500.0
    assert requests.get(f"{FLASK}/detalhes/2").json()["categoria"] == "Monitores"
    assert requests.get(f"{NODE}/estoque/1").json()["nome"] == "Dell XPS 13"
    assert requests.get(f"{NODE}/estoque/2").json()["estoque"] == 5
 
 
def teste_ex1_cliente_integrador():
    texto = formatar_relatorio(buscar_relatorio("1"))
    assert texto == "ID: 1 | Nome: Dell XPS 13 | Preço: R$ 2500.0 | Estoque: 10", texto
 
 
def teste_ex2_proxy():
    dados = requests.get(f"{NODE}/api/full-info/1").json()
    assert dados["nome"] == "Dell XPS 13" and dados["preco"] == 2500.0
 
 
def teste_ex3_status_padronizado():
    resultados = verificar_status([f"{FLASK}/status", f"{NODE}/status"])
    for dados in resultados:
        assert set(dados) == {"service", "status", "timestamp"}
        assert dados["status"] == "online"
 
 
def teste_ex4_cadastro_distribuido():
    produto = {"id": "3", "nome": "teclado", "estoque": 20, "preco_base": 200.0, "categoria": "Perifericos"}
    resp = requests.post(f"{NODE}/cadastrar", json=produto)
    assert resp.status_code == 201, resp.text
    assert requests.get(f"{NODE}/estoque/3").json()["nome"] == "TECLADO"
    fiscal = requests.get(f"{FLASK}/detalhes/3").json()
    assert fiscal["preco"] == 240.0 and fiscal["categoria"] == "Perifericos"   # 200 + 20%
 
 
def teste_ex5_validacao_id():
    esperado = {"error": "INVALID_ID", "message": "O ID deve ser um inteiro positivo"}
    for url in [f"{NODE}/estoque/-5", f"{NODE}/estoque/abc", f"{NODE}/api/full-info/-1",
                f"{FLASK}/detalhes/-5", f"{FLASK}/detalhes/abc"]:
        resp = requests.get(url)
        assert resp.status_code == 400 and resp.json() == esperado, f"{url} -> {resp.status_code}"
 
 
if __name__ == "__main__":  
    testes = [exemplos_aula, teste_preparacao_bases, teste_ex1_cliente_integrador,
              teste_ex2_proxy, teste_ex3_status_padronizado, teste_ex4_cadastro_distribuido,
              teste_ex5_validacao_id]
    aprovados = 0
    for teste in testes:
        try:
            teste()
            print(f"[OK]    {teste.__name__}")
            aprovados += 1
        except AssertionError as e:
            print(f"[FALHA] {teste.__name__}: {e}")
        except requests.ConnectionError:
            print(f"[FALHA] {teste.__name__}: servidor fora do ar")
    print(f"\n{aprovados}/{len(testes)} testes aprovados")
 