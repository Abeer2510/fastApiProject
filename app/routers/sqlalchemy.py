
from typing import List, Optional
from fastapi import HTTPException, Response, status, Depends, APIRouter


from  sqlalchemy.orm import Session
from ..database import get_db
from .. import models

from ..authentication import get_current_user

from ..schemas import Post, PostIn, PostOut

router = APIRouter(
    tags = ["Sqlalchemy"]
)


#only one with searh parameters
@router.get("/sqlalchemy", response_model=List[PostOut])
async def test_sqlalchemy_get(limit = 5, offset = 0, contains: Optional[str] = "",
                              db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(contains)).limit(limit).offset(offset).all()
    return posts




@router.get("/sqlalchemy/{id}", response_model=PostOut)
async def test_sqlalchemy_get_id(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail = "Post Id not found")

    return post




@router.post("/sqlalchemy", response_model=PostOut, )
async def test_sqlalchemy_create(post: PostIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    new_post = models.Post(user_id = user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post




@router.delete("/sqlalchemy/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def test_sqlalchemy_delete_id(id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Post Id not found")
    
    if not user.id == post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to delete this post")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/sqlalchemy/{id}", response_model=PostOut)
async def test_sqlalchemy_put(id: int, post: Post, db: Session = Depends(get_db), user = Depends(get_current_user)):
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_post_query.first()

    if not updated_post:
        raise HTTPException(status_code=404, detail = "Post Id not found")
    
    if not user.id == updated_post.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to update this post")
    
    updated_post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return updated_post