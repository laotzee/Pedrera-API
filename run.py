import os
from app import create_app
from config import config_map
from dotenv import load_dotenv

load_dotenv()
env = os.getenv('FLASK_ENV')
app_env = config_map.get(env, config_map['production'])

app = create_app(app_env)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
