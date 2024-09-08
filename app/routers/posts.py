
from typing import List
from fastapi import Depends, HTTPException, Response, status, APIRouter


from ..database import psycopConnect
from ..schemas import PostIn, PostOut, UserOut

from..authentication import get_current_user

from psycopg2.extras import RealDictRow

router = APIRouter(
    tags = ["Psycopg2"]
)


conn, cursor = psycopConnect()

async def update_users(posts):
    print(type(posts))
    if isinstance(posts, list):
        for post in posts:
            user = await user_by_id_psycopg2(post["user_id"])
            post["user_details"] = user

    elif isinstance(posts, RealDictRow):
            user = await user_by_id_psycopg2(posts["user_id"])
            posts["user_details"] = user

    else:
        raise HTTPException(status_code=400, detail="Invalid data type for posts")



@router.get("/posts", response_model=List[PostOut])
async def get_all_posts():
    cursor.execute("""SELECT* from posts""")
    posts = cursor.fetchall()
    await update_users(posts)
    return posts


@router.get("/my_posts", response_model=List[PostOut],)
async def get_my_posts(user = Depends(get_current_user)):
    cursor.execute("""SELECT* from posts WHERE posts.user_id = %s""", (str(user.id),))
    print(user.created_at)
    posts = cursor.fetchall()
    await update_users(posts)
    return posts



@router.get("/my_posts/{id}", response_model=PostOut)
async def root(id:int, user = Depends(get_current_user)):
    cursor.execute("""SELECT* from posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail = "Post Id not found")
    
    if not post["user_id"] == user.id:
        raise HTTPException(status_code=403, detail = "Not your post")
    
    await update_users(post)
    
    return post


@router.get("/userspsycopg2/{id}", response_model=UserOut)
async def user_by_id_psycopg2(id:int, user = Depends(get_current_user)):
    cursor.execute("""SELECT* from users WHERE id = %s""", (str(id),))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail = "Post Id not found")
    
    return user



@router.get("/posts/{id}", response_model=PostOut)
async def root(id:int, user = Depends(get_current_user)):
    cursor.execute("""SELECT* from posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail = "Post Id not found")
    
    await update_users(post)
    
    return post





@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn, user = Depends(get_current_user)):
    cursor.execute("""INSERT INTO posts (title, content, published, user_id) VALUES (%s, %s, %s, %s) RETURNING *""",
                    (post.title, post.content, post.published, user.id))
    
    post = cursor.fetchone()

    conn.commit()

    await update_users(post)

    return post





@router.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_post(id:int, user = Depends(get_current_user)):
    cursor.execute("""DELETE from posts WHERE id = %s RETURNING*""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail = "Post Id not found")
    
    if not post["user_id"] == user.id:
        raise HTTPException(status_code=403, detail = "You are not authorized to delete this post")
    
    conn.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)





@router.put("/posts/{id}", response_model=PostOut)
async def update_post(id:int, post: PostIn, user = Depends(get_current_user)):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE Id = %s RETURNING *""",
                    (post.title, post.content, post.published, str(id)))

    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail = "Post Id not found")
    
    if not post["user_id"] == user.id:
        raise HTTPException(status_code=403, detail = "You are not authorized to edit this post")

    conn.commit()

    await update_users(post)

    return post