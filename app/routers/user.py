from fastapi import APIRouter, Depends, HTTPException
from app import schemas, models, utils
from starlette import status
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/', response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.CreateUser, db: Session=Depends(get_db)):
    # hash the password
    hashed_password =utils.hash_pass(user.password)
    
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post('/login', response_model=schemas.Token)
def login(userdetails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == userdetails.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="The User does not exist"
        )

    if not utils.verify_password(userdetails.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="The passwords do not match"
        )

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
