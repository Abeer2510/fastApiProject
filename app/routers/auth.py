from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, utils

from .users import user_by_email
from ..authentication import create_access_token, get_current_user

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
async def login_verify(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user_dict = await user_by_email(form_data.username, db)

    if not utils.my_verify(form_data.password, user_dict.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data = {"user_id": user_dict.id})

    return schemas.Token(access_token=access_token, token_type="bearer")



@router.get('/me', response_model=schemas.UserOut)
async def test_token(user: schemas.UserOut = Depends(get_current_user)):
    return user