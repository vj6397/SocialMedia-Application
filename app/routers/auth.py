from sqlalchemy.orm import Session
from .. import  models,schemas,utils,oauth2
from ..database import get_db
from fastapi import Body, Depends, FastAPI,HTTPException,status,Response,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    prefix='/login',
    tags=['Login']
)

@router.post("/")
def login(user_cred:OAuth2PasswordRequestForm=Depends(), db :Session =Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_cred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='invalid credentials')
    
    if not utils.verify(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='invalid credentials')
    
    jwt_token=oauth2.create_access_token(data={"user_id":user.id})

    return {'jwt_token':jwt_token,"token_type":'bearer'}