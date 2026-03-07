from config.init_app import init_app
from dotenv import load_dotenv
from os import getenv
import uvicorn

load_dotenv()

def main():
    app = init_app()

    uvicorn.run(
        app=app, 
        host=getenv('HOST'),
        port=int(getenv('PORT'))
    )

if __name__ == "__main__":
    main()
