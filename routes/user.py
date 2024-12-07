from fastapi import APIRouter, Depends
from schemas.user import User, UserCreate, RolCreate, Userlogin, LoginResponse
from database.db import get_db
from sqlalchemy.orm import Session
from controllers.user import create_user, create_rol, exist_rol, all_roles, exist_user, all_users, verify_credentials, login_output
from utils.auth import generate_token
from fastapi import HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

## Usuarios

#nuevo usuario
@router.post("/", responses={
    200 :{"description": "Petición exitosa","model":list[User]},
    424 :{"description": "Error de dependencia"},
    500 :{"description": "Se jodió el servidor"}
})
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    exist = exist_user(user.email, db)
    if exist:
        return HTTPException(status_code=424,detail="Usuario ya existe")
    new_user = create_user(user,db)
    return User(**new_user.__dict__)


#obtener usuario por id
@router.get("/{mail}")
def get_user(mail: str, db: Session = Depends(get_db)):
    exist = exist_user(mail, db)
    if not exist:
        return JSONResponse(status_code=424,content={"message": "Hubo un error de dependencias","about":"No estas haciendo las cosas bien"})
    return User(**exist.__dict__)
    

#obtener todos los usuarios
@router.get("/all/users", response_model=list[User], responses={
    200 :{"description": "Petición exitosa","model":list[User]},
    424 :{"description": "Error de dependencia"},
    500 :{"description": "Se jodió el servidor"}
})
def get_all_users(db: Session = Depends(get_db)):
    return all_users(db)

# login
@router.post("/login",summary="Este es el sericio para realizar el login de mi aplicacion", 
             description="""# Atenticacion
                         Este es el servicio de autenticación de mi backend desarrollado para la clase de software""")
def autentication(cred:Userlogin, db: Session = Depends(get_db)):
    """
    The function performs user authentication and returns a token if the credentials are verified.
    
    Args:
      cred (Userlogin): The parameter `cred` is of type `Userlogin`, which is likely a data structure or
    class representing user login credentials. It probably has properties such as `email` and
    `password`.
      db (Session): The parameter "db" is of type "Session" and is used to access the database. It is
    likely that the "get_db" function is responsible for creating and returning a database session
    object. This session object is then used to interact with the database, such as querying for user
    credentials or updating
    
    Returns:
      The code is returning either a message stating "User not authenticated" if the user credentials
    are not verified, or a token if the user credentials are verified.
    """
    # The code is performing user authentication.
    result = verify_credentials(cred.email, cred.password, db)

    if not result:
        return {"message": "User not authenticated"}
    else:
        return login_output(cred.email, db)


@router.post("/role")
def create_new_role(new_rol: RolCreate, db: Session = Depends(get_db)):
    exist = exist_rol(new_rol.rol_name, db)
    if exist:
        return HTTPException(status_code=424,detail="rol ya existe")

    rol = create_rol(new_rol, db)
    return rol

@router.get("/all/roles",response_model=list[RolCreate])
def get_all_roles(db: Session = Depends(get_db)):
    return all_roles(db)