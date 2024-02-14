from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

bcrypt = Bcrypt()
db = SQLAlchemy()
cors = CORS()