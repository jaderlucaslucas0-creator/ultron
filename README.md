# HERMES

Assistente pessoal de IA baseado em FastAPI.

## O que já funciona sem OPENAI_API_KEY

- Chat com modo offline
- Memória persistente
- Skills
- Pesquisa web pública
- Arquivos
- Automações
- Interface web responsiva
- Falar com o Hermes usando reconhecimento de voz do navegador
- Respostas por voz usando Speech Synthesis do navegador
- Banco SQLite local ou PostgreSQL no Render

## IA local opcional

Para respostas generativas completas sem API externa, configure um servidor local compatível com Ollama:

```env
LOCAL_AI_URL=http://127.0.0.1:11434
LOCAL_AI_MODEL=llama3.2
```

No Render, um Ollama local não estará disponível automaticamente; nesse caso o Hermes continua operando no modo offline.

## Render

O `render.yaml` já usa:

```
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Nenhuma `OPENAI_API_KEY` é necessária.

## Projeto

A base do projeto continua no repositório original, mas a identidade do assistente agora é **Hermes**.
