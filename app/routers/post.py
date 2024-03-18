from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import oauth2
from .. import  models,schemas
from typing import List, Optional
from ..database import get_db
from fastapi import  Depends, FastAPI,HTTPException,status,Response,APIRouter

router=APIRouter(
    prefix='/posts',
    tags=['Posts']
)





# Get all posts
@router.get("/",response_model=List[schemas.post_out])
def posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
          ,limit:int=3,skip:int=0,search:Optional[str]=""):

    #post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # record=conn.execute("""Select * from posts """).fetchall()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return post




# Get particular post
@router.get("/{id}",response_model=schemas.post_out)
def get_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    
    # post = conn.execute("""select * from posts where id=%s """, (id,)).fetchone()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # print(current_user.email)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post was not found')
    return post
    



# POST API with pydantic
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.post_response)
def create_post(new_post:schemas.create_post,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post_dict=new_post.model_dump()
    # post_dict['id']=randrange(0,10000000)
    # mypost.append(post_dict)

    # record=conn.execute(""" Insert into posts (title,content, published) Values (%s,%s,%s) RETURNING *""", 
    #                     (new_post.title,new_post.content,new_post.published)).fetchone()
    # conn.commit()
    post=models.Post(owner_id=current_user.id,**new_post.model_dump())    #it breaks data accordingly
    # or can access like new_post.title,...
    db.add(post)
    db.commit()
    db.refresh(post)
    return post




#delete post
@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # record=conn.execute(""" delete from posts where id=%s returning *""" ,(id,)).fetchone()
    # conn.commit()
    record=db.query(models.Post).filter(models.Post.id==id)
    if record.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post not found')
    
    if record.first().id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Unautherised to delete others post')

    record.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



#update post
@router.put('/{id}',response_model=schemas.post_response)
def update_post(id:int,post:schemas.create_post,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post_dict=post.model_dump()
    # post_dict['id']=id
    # mypost[index]=post_dict

    # record=conn.execute(""" update posts set title=%s , content=%s, published=%s where id=%s returning *""",
    #                     (post.title,post.content,post.published,str(id),) ).fetchone()
    # conn.commit()
    
    record=db.query(models.Post).filter(models.Post.id==id)
    new_post=record.first()
    if new_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='post not found')
    
    if new_post.id!= current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Unautherised to update others post')
    
    record.update(post.model_dump(),synchronize_session=False)
    db.commit()

    return record.first()