from config.init_app import init_app
from config.settings import settings
import uvicorn

def main():
    app = init_app()

    uvicorn.run(
        app=app, 
        host=settings.server_host,
        port=settings.server_port
    )

if __name__ == "__main__":
    main()
