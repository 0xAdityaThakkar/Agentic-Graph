# main.py
from dotenv import load_dotenv
from fastapi import FastAPI
from src.controller import routes

load_dotenv()
app = FastAPI()

# Include the router from the items module
app.include_router(routes.router)
