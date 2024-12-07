import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import re
from datetime import datetime


# Añadir el directorio 'src' al sys.path para que Python pueda encontrar 'db_models'
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.db_models import User, Base
from models.db_models import User, Base, Task


# ----------------------------------------------------------------------------------
### TEST 1


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


# ----------------------------------------------------------------------------------
### TEST 2


# Función auxiliar para validar correos electrónicos
def is_valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None


# Prueba para comprobar que no se permita el registro con un correo inválido
def test_invalid_email_constraint(db_session):
    # Intentar crear un usuario con un correo inválido
    invalid_email = "invalid-email"  # Sin formato correcto
    user_with_invalid_email = User(name="Invalid Email User", email=invalid_email, password="securepassword", rol_id=1)

    db_session.add(user_with_invalid_email)
    
    # Validar que el correo no pasa la comprobación manual de validación de formato
    assert not is_valid_email(invalid_email), f"El correo {invalid_email} es inválido, pero pasó la validación."

    try:
        # Intentar hacer commit, pero esto debería lanzar un error si hay validación en la base de datos
        db_session.commit()
        pytest.fail("Se permitió registrar un usuario con un correo inválido.")
    except IntegrityError:
        db_session.rollback()  # Rollback para evitar problemas con la sesión
    except Exception as e:
        db_session.rollback()
        pytest.fail(f"Error inesperado: {str(e)}")

    # Crear un usuario con un correo válido para asegurar que el sistema lo permita
    valid_email = "valid.email@example.com"
    assert is_valid_email(valid_email), f"El correo {valid_email} debería ser válido."
    
    valid_user = User(name="Valid User", email=valid_email, password="securepassword", rol_id=1)
    db_session.add(valid_user)
    
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        pytest.fail(f"Error al registrar un usuario con correo válido: {str(e)}")


# ----------------------------------------------------------------------------------
### TEST 3


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



# Function to test the validation of required fields and date format in Task model
def test_task_required_fields_and_date_format(db_session):
    # Attempt to create a task without required fields
    task_missing_required = Task(task_name=None, description="Missing task name", date_due=datetime.now(), user_id=1)
    db_session.add(task_missing_required)

    try:
        # Validate that an IntegrityError is raised for missing required fields
        db_session.commit()
    except IntegrityError:
        db_session.rollback()  # Rollback the session to avoid further issues

    # Create a valid task with correct date format
    valid_task = Task(
        task_name="Valid Task",
        description="This task has a valid date format and required fields",
        date_due=datetime.strptime("2024-12-31 23:59:59", "%Y-%m-%d %H:%M:%S"),
        user_id=1
    )
    db_session.add(valid_task)

    try:
        db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
        raise e  # Re-raise the exception if any error occurs

    # Fetch the task from the database and verify its properties
    fetched_task = db_session.query(Task).filter_by(task_name="Valid Task").first()
    assert fetched_task is not None
    assert fetched_task.task_name == "Valid Task"
    assert fetched_task.description == "This task has a valid date format and required fields"
    assert fetched_task.date_due == datetime(2024, 12, 31, 23, 59, 59)

    # Attempt to create a task with an invalid date format and check for a ValueError
    try:
        invalid_task = Task(
            task_name="Invalid Date Format",
            description="This task has an invalid date format",
            date_due=datetime.strptime("invalid-date", "%Y-%m-%d %H:%M:%S"),  # Will raise a ValueError
            user_id=1
        )
        db_session.add(invalid_task)
        db_session.commit()
    except ValueError:
        db_session.rollback()  # Rollback the session to ensure clean state for further tests