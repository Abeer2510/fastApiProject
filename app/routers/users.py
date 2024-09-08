
from typing import List
from fastapi import HTTPException, Response, status, Depends, APIRouter


from  sqlalchemy.orm import Session
from ..database import get_db
from .. import models

from ..utils import my_hash

from ..schemas import UserIn, UserOut


router = APIRouter(
    tags=["user"]
)




@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserIn, db: Session = Depends(get_db)):
    #hash
    user.password = my_hash(user.password)

    existing_account = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_account:
        raise HTTPException(status_code=409, detail = "Email already registered")

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get("/user_by_id/{id}", response_model=UserOut)
async def user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail = "User Id not found")

    return user



@router.get("/user_by_email/{email}", response_model=UserOut)
async def user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail = "User Id not found")

    return user