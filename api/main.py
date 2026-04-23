import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import index as indexRoute
from api.models import model_loader
from api.dependencies.config import conf
from api.dependencies.database import Base, engine

app = FastAPI(
    title="Food Delivery API",
    description="REST API for a food delivery and ordering system.",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)
