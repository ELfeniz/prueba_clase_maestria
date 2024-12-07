from fastapi import FastAPI
from database.db import Base, engine
from routes.user import router
from routes.task import router_tasks


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion de Tareas",
            description="Este proyecto consiste en un sistema de Gestion de Tareas con metodologias Agiles para la materia Proceso y Metodologias de Ingenieria de Software",
            version="0.2.0")

app.include_router(router, tags=["User"])

app.include_router(router_tasks, tags=["Task"])