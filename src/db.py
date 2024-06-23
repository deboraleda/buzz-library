from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from . import app
from flask_migrate import Migrate

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DBURI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
