from typing import List
from .models import Post
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def my_hash(password: str):
    return pwd_context.hash(password)

def my_verify(password: str, hashed_password:str):
    return pwd_context.verify(password, hashed_password)



def getPost(id:str, posts: List[Post]):
    for post in posts:

        if post["id"] == id:
            return post
        
    
def getIndex(id:str, posts: List[Post]):
    for index, post in enumerate(posts):
        if post["id"] == id:
            print("SUCCESS")
            return index