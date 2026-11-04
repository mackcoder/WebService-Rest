import requests

URL_FLASK = "http://localhost:5000"
URL_NODE = "http://localhost:3000"

def buscar_relatorio(id_produto):
    fiscal = requests.get(f"{URL_FLASK}/detalhes/{id_produto}", timeout=5)
    estoque = requests.get(f"{URL_NODE}/estoque/{id_produto}", timeout=5)
    fiscal.raise_for_status()
    estoque.raise_for_status()
    return {**fiscal.json(), **estoque.json()}

def formatar_relatorio(dados):
    return (f"ID: {dados['id']} | Nome: {dados['nome']} | "
            f"Preço: R$ {dados['preco']} | Estoque: {dados['estoque']}")


def verificar_status(urls):
    resultados = []

    for url in urls:
        try:
            dados = requests.get(url, timeout = 5).json()
            print(f"{dados['service']:<15} | {dados['status']:<7} | {dados['timestamp']}")

            resultados.append(dados)

        except Exception:
            print(f"{url:<15} | offline")
            resultados.append({"service": url, "status": "offline", "timestamp": None})

    return resultados

if __name__ == "__main__":
    id_produto = input("Digite o ID do produto: ").strip()
    try:
        print(formatar_relatorio(buscar_relatorio(id_produto)))
    except requests.HTTPError as e:
        print(f"Erro: {e.response.status_code} - {e.response.json().get('message')}")
    except requests.ConnectionError:
        print("Erro: um dos servidores está fora do ar.")
 
    print("\n--- Status dos servidores ---")
    verificar_status(["http://localhost:5000/status", "http://localhost:3000/status"])  
