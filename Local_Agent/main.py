import os
import subprocess
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Dependências ausentes. Execute 'pip install -r requirements.txt'.")
    sys.exit(1)


def fetch_url(url: str) -> str:
    """Faz download de uma página e retorna o título."""
    resp = requests.get(url, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.title.string if soup.title else "Sem título"


def run_command(cmd: str) -> str:
    """Executa um comando local e retorna a saída."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip() or result.stderr.strip()


def main():
    print("Local_Agent iniciado. Digite 'exit' para sair.")
    while True:
        user_input = input('> ').strip()
        if user_input.lower() == 'exit':
            break
        elif user_input.startswith('http'):
            try:
                title = fetch_url(user_input)
                print(f'Título da página: {title}')
            except Exception as e:
                print(f'Erro ao buscar URL: {e}')
        else:
            output = run_command(user_input)
            print(output)


if __name__ == '__main__':
    main()
