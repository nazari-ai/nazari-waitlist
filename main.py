import uvicorn
import re
import models, schemas
from json import load
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from send_mail import send_email
from database import get_db
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware


rg = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

app = FastAPI(title='ASAlytics Waitlist')
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
    
def commit_user(db:Session, request: schemas.UserCreate):
    new_user= models.User(username= request.username, email= request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def check_user_by_email(db:Session, email:str):
    user = db.query(models.User).filter(models.User.email == email).one_or_none()
    return user


@app.post("/")
async def main(request: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    username, email= request.username, request.email
    db_user= check_user_by_email(db, email= request.email)
    if db_user:
        raise HTTPException(status_code=404, detail="User Already Exists")
    elif (re.search(rg, email)):
        background_tasks.add_task(send_email(subject= "Welcome to ASAlytics🤗", email_to= email, username= username))
        commit_user(db, request)
        raise HTTPException(status_code=200, detail="Success")
    raise HTTPException(status_code=404, detail="Enter a valid email address")

