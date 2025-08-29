# Local_Agent

Este projeto demonstra um agente local executado em um container Docker. O agente
aceita comandos em texto (e opcionalmente por voz) para interagir com o sistema e
consultar a internet (por meio de scraping ou requisições HTTP).

## Estrutura
- `main.py` – ponto de entrada do agente.
- `requirements.txt` – dependências de Python usadas no projeto.
- `Dockerfile` – configura a imagem Docker para executar o agente.
- `flowchart.md` – fluxograma com a lógica básica do agente.

## Uso rápido
```bash
# Build da imagem
docker build -t local_agent .

# Execução interativa
docker run -it local_agent
```

A primeira execução pode demorar caso seja necessário baixar as dependências.
