from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from posts.models import Post
from templating import templates
from users.models import User

router = APIRouter(include_in_schema=False)

@router.get("/users/{user_id}/posts", name="user_posts")
def user_posts_page(
    request: Request, user_id: int, db: Annotated[Session, Depends(get_db)]
):
    result = db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    result = db.execute(select(Post).where(Post.user_id == user_id))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )
