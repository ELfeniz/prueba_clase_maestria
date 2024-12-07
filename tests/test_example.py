import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models.db_models import User


# Prueba para validar que no se permite registrar usuarios con correos duplicados
def test_unique_email_constraint(db_session):
    # Crear el primer usuario con un correo electrónico
    user1 = User(name="John Doe", email="john.doe@example.com", password="securepassword", rol_id=1)
    db_session.add(user1)
    db_session.commit()

    # Intentar crear un segundo usuario con el mismo correo
    user2 = User(name="Jane Doe", email="john.doe@example.com", password="anotherpassword", rol_id=1)
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()  # Esto debería lanzar una excepción debido a la restricción UNIQUE
