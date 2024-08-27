from typing import List
from fastapi import HTTPException, Depends, APIRouter
from starlette import status
from app import models, schemas
from app.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostBase])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    
    return posts

@router.post('/', response_model=List[schemas.CreatePost], status_code=status.HTTP_201_CREATED)
def post_sent(post_post:schemas.CreatePost, db: Session=Depends(get_db)):
    new_post = models.Post(**post_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return [new_post]

@router.get('/{post_id}', response_model=schemas.PostBase, status_code=status.HTTP_200_OK)
def get_post(post_id:int, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    # if the post is not found raise 404
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found!')

    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)


    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The id: {id} you requested for does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()



@router.put('/posts/{id}', response_model=schemas.CreatePost)
def update_post(update_post:schemas.PostBase, id:int, db:Session = Depends(get_db)):

    updated_post =  db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
    updated_post.update(update_post.model_dump(), synchronize_session=False)
    db.commit()


    return  updated_post.first()