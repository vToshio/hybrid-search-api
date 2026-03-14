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