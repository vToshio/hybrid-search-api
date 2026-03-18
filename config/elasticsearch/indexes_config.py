from os import getenv

documents_index_body = {
    'settings': {
        'number_of_shards': getenv('ES_SHARDS_NUMBER', 1),
        'number_of_replicas': getenv('ES_REPLICAS_NUMBER', 0)
    },
    'mappings': {
        'properties': {
            'name': { 'type': 'text' },
            'content': { 'type': 'text' },
            'embeddings': { 
                'type': 'dense_vector', 
                'dims': 768,            
                'index': True,
                'similarity': 'cosine' 
            }
        }
    }
}

documents_index_body_v2 = {
    'settings': {
        'number_of_shards': getenv('ES_SHARDS_NUMBER', 1),
        'number_of_replicas': getenv('ES_REPLICAS_NUMBER', 0),
        
        # Configurando os parâmetros do BM-25
        'index': {
            'similarity': {
                'default': {
                    'type': 'BM25',
                    'b': 0.6,
                    'k1': 1.5
                }
            }
        },
        
        # Configurando um analyzer para identificar palavras em portugues
        'analysis': {
            'analyzer': {
                'portuguese': {
                    'type': 'standard',
                    'stopwords': '_portuguese_'
                }
            }
        }
    },

    # Mapeando os campos do índice documents
    'mappings': {
        'properties': {
            'document_name': { 'type': 'keyword' },
            'content': { 'type': 'text', 'analyzer': 'portuguese' },
            'chunk_id': { 'type': 'integer' },
            
            # Configurando o embedding
            'embeddings': {
                'type': 'dense_vector',
                'dims': int(getenv('HF_MODEL_DIMS', 768)),
                'similarity': 'cosine',
                'index': True,
                'index_options': {
                    'type': 'bbq_hnsw'
                }
            }
        }
    }
}