from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
  # id, username, password
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  role = db.Column(db.String(50), nullable=False, default='user') 