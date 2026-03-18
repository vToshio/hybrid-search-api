from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000
    debug: bool = False
    
    elastic_url: str 
    es_shards_number: int = 1
    es_replicas_number: int = 0

    hf_token: str
    hf_model: str = 'all-mpnet-base-v2'
    hf_model_dims: int = 768

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8'
    )

settings = Settings()