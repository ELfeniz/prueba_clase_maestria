from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    rol_id: int

class UserCreate(User):
    password: str

class RolCreate(BaseModel):
    rol_name: str

class RolOut(RolCreate):
    rol_id: int

class Userlogin(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    rol_id: int
    user_id: int
    name: str
