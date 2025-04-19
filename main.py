#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from db import Base, engine, SessionLocal, get_db
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from user import UserDB, UserCreate, User, Token
from security import *
from recipe.route import recipe_router
app = FastAPI(title='Recipe API', description='My Recipe API', version='0.0.1') 
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
Base.metadata.create_all(bind=engine)


@app.post("/users/", response_model=User, status_code=201)
async def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = await get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await create_user_db(db, user)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = await get_user_by_username(db, username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: UserDB = Depends(get_current_active_user)):
    return current_user

@app.get("/protected/", dependencies=[Depends(get_current_active_user)])
async def protected_route():
    return {"message": "This route is protected!"}

@app.get("/public/")
async def public_route():
    return {"message": "This route is public."}
	
app.include_router(recipe_router, tags=['recipe'])
# if __name__ == '__main__':
# 	uvicorn.run('main:app', host='0.0.0.0', port=8080, reload=True)
