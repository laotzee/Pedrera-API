import os
from app import create_app
from config import config_map
from dotenv import load_dotenv

load_dotenv()
env = os.getenv('FLASK_ENV')
app = create_app(env)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
