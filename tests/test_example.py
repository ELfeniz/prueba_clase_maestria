import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Añadir el directorio 'src' al sys.path para que Python pueda encontrar 'db_models'
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.db_models import User, Base


# Configuración de la base de datos en memoria para pruebas
@pytest.fixture(scope="function")
def db_session():
    # Crear un motor SQLite en memoria
    engine = create_engine("sqlite:///:memory:")
    
    # Crear las tablas
    Base.metadata.create_all(engine)
    
    # Crear una sesión para interactuar con la base de datos
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session  # Devuelve la sesión para ser utilizada en la prueba
    
    # Cerrar la sesión y liberar los recursos después de la prueba
    session.close()
    engine.dispose()


# Prueba para validar que no se permite registrar usuarios con correos duplicados
def test_unique_email_constraint(db_session):
    # Crear el primer usuario con un correo electrónico
    user1 = User(name="John Doe", email="john.doe@example.com", password="securepassword", rol_id=1)
    db_session.add(user1)
    db_session.commit()

    # Intentar crear un segundo usuario con el mismo correo
    user2 = User(name="Jane Doe", email="john.doe@example.com", password="anotherpassword", rol_id=1)
    db_session.add(user2)

    # Validar que se lanza una excepción IntegrityError
    with pytest.raises(IntegrityError):
        db_session.commit()  # Esto debería lanzar una excepción debido a la restricción UNIQUE
