# main.py
from fastapi import FastAPI
from src.router import routes

app = FastAPI()

# Include the router from the items module
app.include_router(routes.router)
