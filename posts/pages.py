from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from posts.models import Post
from templating import templates

router = APIRouter(include_in_schema=False)


@router.get("/", name="home")
@router.get("/posts", name="posts")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Post))
    posts = result.scalars().all()
    context = {"posts": posts, "title": "Home"}
    return templates.TemplateResponse(request, "home.html", context=context)


@router.get("/post/{post_id}", name="post")
def post_page(request: Request, post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Post).where(Post.id == post_id))
    posts = result.scalars().first()
    for post in posts:
        if post.get("id") == post_id:
            context = {
                "post": post,
                "title": post["title"][:50],
            }
            return templates.TemplateResponse(request, "post.html", context=context)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
