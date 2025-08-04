from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.login_register import loginRouter
from app.routers.perfil import perfilRouter
from app.routers.privacidad import privacidadRouter
from app.routers.materias import materiasRouter


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loginRouter)
app.include_router(perfilRouter)
app.include_router(privacidadRouter)
app.include_router(materiasRouter)


@app.get("/")
def index():
    return {"data": "Hello world!"}


if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
