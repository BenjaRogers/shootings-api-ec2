from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv, dotenv_values
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from DB.models import db

app = Flask(__name__)

CORS(app)
migrate = Migrate()

load_dotenv()  # load .env values
env_vars = dotenv_values("API/.env")  # assign .env values to dict var
      
# configure app with .env values
app.config["SECRET_KEY"] = env_vars["secret_key"]
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{env_vars['DB_USER']}:{env_vars['DB_PASS']}@localhost/{env_vars['DB_NAME']}"
db.init_app(app)
migrate.init_app(app, db)
