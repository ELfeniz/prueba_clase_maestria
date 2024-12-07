from schemas.user import UserCreate, RolCreate
from models.db_models import User, Rol
from utils.auth import generate_token


def create_user(new_user: UserCreate, db):

    usr = User(**new_user.model_dump())
    ## Acá va la logica de consulta en la base de datos
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr

def exist_user(email: str, db):
    usr = db.query(User).filter(User.email == email).first()
    return usr

def all_users(db):
    return db.query(User).all()

def verify_credentials(email: str, password: str, db) -> bool:
    result = db.query(User).filter(User.email == email).first()
    if result is None:
        return False
    return result.password == password

def create_rol(new_rol: RolCreate, db):
    ## Acá va la logica de consulta en la base de datos

    rol = Rol(**new_rol.model_dump())
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol

def exist_rol(rol_name: str, db):
    rol = db.query(Rol).filter(Rol.rol_name == rol_name).first()
    return rol

def all_roles(db):
    return db.query(Rol).all()

def login_output(email: str, db):
    # Query specific columns
    columns = ["user_id", "name","rol_id"]
    user_data = db.query(*[getattr(User, col) for col in columns]).filter(User.email == email).first()

    # Generate a token (replace with your token generation logic)
    token = generate_token()

    # Return the result as a dictionary
    if user_data:
        return {
            "user": {col: value for col, value in zip(columns, user_data)},
            "token": token,
        }