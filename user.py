from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
from typing import Optional

app = FastAPI()

# PostgreSQL Database Setup
DATABASE_URL = "postgresql://admin:123456@localhost/user"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Setup
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["user_profiles"]
profile_collection = mongo_db["profiles"]

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    first_name: str
    email: str
    phone: str
    password: str

class UserProfile(BaseModel):
    first_name: str
    email: str
    phone: str
    profile_picture: Optional[str] = None

@app.post("/register-user/")
def register_user(user: UserCreate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    profile_picture = user.profile_picture or ""
    profile_collection.insert_one({"user_id": new_user.id, "profile_picture": profile_picture})
    
    db.close()
    return {"message": "User registered successfully"}

@app.get("/user-profile/{user_id}")
def get_user_profile(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = profile_collection.find_one({"user_id": user.id})
    
    db.close()
    return UserProfile(
        first_name=user.first_name,
        email=user.email,
        phone=user.phone,
        profile_picture=profile["profile_picture"] if profile else None
    )

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
from typing import Optional

app = FastAPI()

# PostgreSQL Database Setup
DATABASE_URL = "postgresql://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Setup
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["user_profiles"]
profile_collection = mongo_db["profiles"]

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UserCreate(BaseModel):
    first_name: str
    email: str
    phone: str
    password: str

class UserProfile(BaseModel):
    first_name: str
    email: str
    phone: str
    profile_picture: Optional[str] = None

@app.post("/register-user/")
def register_user(user: UserCreate):
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    profile_picture = user.profile_picture or ""
    profile_collection.insert_one({"user_id": new_user.id, "profile_picture": profile_picture})
    
    db.close()
    return {"message": "User registered successfully"}

@app.get("/user-profile/{user_id}")
def get_user_profile(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")
    
    profile = profile_collection.find_one({"user_id": user.id})
    
    db.close()
    return UserProfile(
        first_name=user.first_name,
        email=user.email,
        phone=user.phone,
        profile_picture=profile["profile_picture"] if profile else None
    )
