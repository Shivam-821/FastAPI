from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import engine, get_db
from .. import models, schema, utils, oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_post(post: schema.CreatePost, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    
    # post.dict()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    new_post = models.Post(user_id=user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# to get all our own posts
@router.get('/', response_model=List[schema.PostResponse])
def get_post(db: Session = Depends(get_db), user = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str | None= None):
    posts = db.query(models.Post).filter(user.id == models.Post.user_id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.get('/{id}', response_model=schema.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter((models.Post.id == id) & (models.Post.user_id == user.id)).first()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} was not found')

    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform the requested operation')

    return post

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested operation")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', response_model=schema.PostResponse)
def update_post(id: int, post: schema.CreatePost, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post_exist = post_query.first()

    if post_exist == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post_exist.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested operation")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
