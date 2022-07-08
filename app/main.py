# app/main.py
from http.client import HTTPException
from fastapi import FastAPI

from app.db import database, User, UserCreate, Report

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def auth_user(email, password):
    user = User.get_by_email(email)
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user

app = FastAPI(title="Service Reportr", description="Service Reportr API", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/user")
async def create_user(user: UserCreate):
    hashed_pass = get_password_hash(user.password)
    user = User.get_by_email(user.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=user.email, password=hashed_pass, fname=user.fname, lname=user.lname)
    await user.save()
    return user

@app.get("/user")
async def get_users():
    return await User.objects.select_related(User.reports).filter(active=True).all()

@app.post("/report")
async def create_report(report: Report):
    await report.save()
    return report

@app.get("/report")
async def get_reports():
    return await Report.objects.all()

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy user
    await User.objects.get_or_create(email="test@test.com", fname="Test", lname="User")
    await Report.objects.get_or_create(user=1, service_hours=10, service_mintues=15, placements=3, videos=0, return_visits=4, bible_studies=1, notes="Conducted a bible study with Jim in June")

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
