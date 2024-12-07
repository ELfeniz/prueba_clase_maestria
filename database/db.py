from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

'''
This file the connection to the MySQL dataset using sqlalchemy with a local dataframe the password is on the .env file
'''
# Cargar variables de entorno desde el archivo .env
load_dotenv('.env')

# Obtener la URL de conexión desde la variable de entorno
DATABASE_URL = "postgresql+psycopg2://admin:admin1234@postgres:5432/Tareas"


# Configuración de SQLAlchemy con PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)
conn = engine.connect()

# Configurar sesión y base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()