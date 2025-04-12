from datetime import timedelta
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from mspt.apps.users import crud
from mspt.settings.utils import  get_db
from mspt.settings.security import get_current_user, get_password_hash
from mspt.settings import config
from mspt.settings.jwt import create_access_token
from mspt.apps.users.models import User as DBUser
from mspt.apps.common.schemas.msg import Msg
from mspt.apps.users.schemas import User
from mspt.utils.token import (
    generate_password_reset_token,
    verify_password_reset_token,
)
from mspt.utils.email import (
    send_reset_password_email,
)

from mspt.apps.common.schemas.token import Token
from mspt.apps.users.schemas import UserLoginExtras

class TokenWithExtras(Token, UserLoginExtras):
    pass

router = APIRouter()


@router.post("/login/access-token", response_model=TokenWithExtras, tags=["login"])
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_uid": user.uid}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "uid": user.uid,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
    }


@router.post("/login/test-token", tags=["login"], response_model=User)
def test_token(current_user: DBUser = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", tags=["login"], response_model=Msg)
def recover_password(email: str, db: Session = Depends(get_db)):
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", tags=["login"], response_model=Msg)
def reset_password(token: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)):
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
