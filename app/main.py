# app/main.py
from fastapi import FastAPI

from app.db import database, User

app = FastAPI(title="Service Reportr", description="Service Reportr API", version="0.1.0")

@app.get("/")
async def root():
    return await User.objects.all()

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy user
    await User.objects.get_or_create(email="test@test.com")

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
