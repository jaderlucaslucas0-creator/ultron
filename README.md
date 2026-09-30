# 🤖 ULTRON V2

MVP do assistente pessoal de IA ULTRON.

## MVP implementado

- FastAPI modular
- Interface web responsiva
- Chat com modelo compatível com OpenAI
- Memória persistente
- Sistema inicial de Skills
- Skill de calculadora segura
- Orquestrador
- PostgreSQL em produção e SQLite local
- API REST
- Health check
- Autenticação opcional por Bearer token
- Configuração para Render
- Separação entre backend e frontend

## Estrutura

~~~text
main.py
app/
  api/
  brain/
  core/
  database/
  skills/
frontend/
requirements.txt
render.yaml
.env.example
README.md
~~~

## Executar localmente

Python 3.11+ recomendado.

~~~bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload
~~~

Abra http://127.0.0.1:8000.

Configure OPENAI_API_KEY no .env para conversar com o modelo. Se ULTRON_API_KEY for configurada, informe o token no campo API Key da interface.

## Variáveis de ambiente

- OPENAI_API_KEY
- OPENAI_MODEL
- OPENAI_BASE_URL
- DATABASE_URL
- ULTRON_API_KEY
- CORS_ORIGINS

Nunca envie .env para o GitHub.

## API

- GET /health
- GET /api/status
- POST /api/chat
- GET /api/memory
- POST /api/memory
- DELETE /api/memory/{memory_id}
- GET /api/skills

## Render

O arquivo render.yaml prepara um Web Service e um PostgreSQL.

1. Conecte o repositório ao Render.
2. Configure OPENAI_API_KEY.
3. Opcionalmente configure OPENAI_BASE_URL e ULTRON_API_KEY.
4. Faça o deploy.
5. Teste /health.
6. Abra a URL do serviço.

O projeto não usa polling artificial, requisições falsas ou mecanismos para impedir suspensão. Para disponibilidade contínua, use uma infraestrutura/plano do Render que mantenha o Web Service ativo.

## Arquitetura

O frontend chama somente a API. O cérebro, memória, Skills e banco ficam no backend. Isso permite futuramente conectar Android, Windows e outros clientes sem reconstruir o núcleo.

## Próximas fases

Somente depois de validar este MVP:

1. Voz, STT, TTS e Wake Word.
2. Pesquisa web, arquivos, visão e automações.
3. Agentes especializados e plugins.
4. Aplicativos Android e Windows.
