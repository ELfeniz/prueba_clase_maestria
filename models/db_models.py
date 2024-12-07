from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database.db import Base
from sqlalchemy.orm import validates
import re

"""
This file contains the structure of the outputs on the API response.
"""

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    rol_id = Column(Integer, ForeignKey("roles.rol_id"))

    rol = relationship("Rol", back_populates="users")
    tasks = relationship("Task", back_populates="user")  # Fixed relationship name

    @validates('email')
    def validate_email(self, key, email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, email):
            raise ValueError(f"Correo inválido: {email}")
        return email

class Rol(Base):
    __tablename__ = "roles"

    rol_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rol_name = Column(String(100), nullable=False)

    users = relationship("User", back_populates="rol")


class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    task_name = Column(String, nullable=False)
    description = Column(String)
    date_due = Column(DateTime)
    status = Column(Boolean, server_default='f', default=False)  # Default Boolean value

    user = relationship("User", back_populates="tasks")
