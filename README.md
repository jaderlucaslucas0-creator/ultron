# ULTRON AI

Assistente pessoal local-first inspirado em arquiteturas de agentes modernas.

## Objetivo
- Conversa por texto sem OpenAI obrigatória
- Ollama opcional para IA local
- Arquitetura de agentes
- Pesquisa web
- Memória local
- Interface futurista
- Backend compatível com Render

## Rodar localmente
1. Instale Python 3.11+.
2. `pip install -r requirements.txt`
3. Copie `.env.example` para `.env`.
4. Execute `python main.py`.
5. Abra `http://localhost:8000`.

Para IA local, instale Ollama e configure `OLLAMA_MODEL`.

> O controle do computador será executado por um agente local separado. O servidor Render não recebe acesso direto ao seu Windows.
