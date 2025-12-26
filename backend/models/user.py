from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from .db import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    todos = relationship('Todo', back_populates='user', cascade='all, delete-orphan')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def __repr__(self):
        return f'<User {self.name}>'