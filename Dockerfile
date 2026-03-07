# Imagem base Python
FROM python:3.13-slim

# Instala o uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Diretório da aplicação
WORKDIR /app

# Copia arquivos de dependências primeiro (melhora cache)
COPY pyproject.toml uv.lock ./

# Instala dependências
RUN uv sync --frozen --no-cache

# Copia o restante da aplicação
COPY . .

# Porta padrão (ex: FastAPI)
EXPOSE 8000

# Comando de execução
CMD ["uv", "run", "main.py"]