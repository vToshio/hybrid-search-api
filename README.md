# Pesquisa Híbrida - API 🚀

Este repositório contém o protótipo da API desenvolvida para o meu Trabalho de Conclusão de Curso (TCC) em Sistemas de Informação na **Fundação Hermínio Ometto (FHO)**.

A aplicação implementa uma API RESTful que utiliza técnicas avançadas de **Processamento de Linguagem Natural (NLP)** para realizar buscas híbridas. O sistema fragmenta documentos em *chunks*, gera representações vetoriais (*embeddings*) e os indexa para permitir recuperações que combinam a precisão da busca textual com a semântica da busca vetorial.

## 🛠️ Tecnologias e Ferramentas

* **Python & FastAPI:** Framework para construção da API assíncrona com documentação automática (Swagger).
* **LangChain (Text-Splitters):** Utilizado para a segmentação inteligente de documentos em pedaços semanticamente coesos (chunks).
* **Sentence Transformers:** Interface para modelos do Hugging Face. Utiliza o modelo `multilingual-e5-base` (768 dimensões) para geração de vetores densos.
* **Elasticsearch:** Motor de busca e banco de dados vetorial (Vector Store) responsável pela indexação e execução do algoritmo de busca híbrida.
* **Docker & Docker Compose:** Orquestração do ambiente, garantindo que a API e o Elasticsearch rodem em containers isolados.

## 🔍 Como funciona a Pesquisa Híbrida?
O diferencial deste projeto é a combinação de dois métodos de recuperação:
1.  **Busca Full-Text (BM25):** Encontra correspondências exatas de palavras-chave.
2.  **Busca Vetorial (KNN):** Encontra trechos pelo contexto semântico, mesmo que não usem as mesmas palavras da pergunta.

---

## 🚀 Como testar localmente

### Pré-requisitos
* Docker e Docker Compose instalados.
* [uv](https://github.com/astral-sh/uv) (opcional, para gerenciamento de pacotes local).

### Passo a passo

```bash
# 1. Clonar o repositório
git clone [https://github.com/vToshio/hybrid-search-api.git](https://github.com/vToshio/hybrid-search-api.git)
cd hybrid-search-api

# 2. Sincronizar dependências locais (opcional)
uv sync

# 3. Construir e levantar o ambiente com Docker
docker compose up --build
```