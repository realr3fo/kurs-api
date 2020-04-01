import os

from app import app

from dotenv import load_dotenv

load_dotenv()

config_name = os.getenv('APP_SETTINGS') # config_name = "development"
app = app(config_name)

if __name__ == '__main__':
    app.run()
