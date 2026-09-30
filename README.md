# ULTRON V3

Assistente pessoal de IA modular, preparado para rodar no Render.

## Fase 3
- Pesquisa web via ferramenta de busca do modelo.
- Visão: análise de imagens por IA.
- Upload e download de arquivos persistidos no banco.
- Painel de automações com criação, ativação/pausa e exclusão.
- Fase 1 mantida: FastAPI, chat, memória, Skills, logs, PostgreSQL/SQLite, health e Render.
- Fase 2 mantida: STT, TTS e microfone no navegador.

## Variáveis
Configure no Render:
- `OPENAI_API_KEY`
- `DATABASE_URL` para PostgreSQL em produção
- `ULTRON_API_KEY` opcional
- `RESEARCH_MODEL` e `VISION_MODEL` se quiser trocar os modelos

## Render
Build Command:
`pip install -r requirements.txt`

Start Command:
`uvicorn main:app --host 0.0.0.0 --port $PORT`

Health:
`/health`

## Desenvolvimento
`pip install -r requirements.txt`
`uvicorn main:app --reload`

Nunca coloque chaves de API no código ou no Git.
