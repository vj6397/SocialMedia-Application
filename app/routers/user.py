from sqlalchemy.orm import Session
from .. import  models,schemas,utils
from ..database import get_db
from fastapi import Body, Depends, FastAPI,HTTPException,status,Response,APIRouter

router=APIRouter(
    prefix='/users',
    tags=['Users']
)



# User

#create user
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.user_out)
def create_user(user:schemas.user,db: Session = Depends(get_db)):
    new_user=models.User(**user.model_dump())    #it breaks data accordingly
    # or can access like new_post.title,...
    hash_pwd=utils.hash(new_user.password)
    new_user.password=hash_pwd

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#get user
@router.get('/{id}',response_model=schemas.user_out)
def get_user(id:int, db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='user not found')
    return user