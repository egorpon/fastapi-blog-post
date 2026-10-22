from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

posts: list[dict] = [
    {
        "id": 1,
        "title": "I love a Harry Potter, and that's why...",
        "date_posted": "april 20, 2025",
        "author": "Egor",
        "content": "eodjakdasjdkadkjaskjdkjasjdka",
    },
    {
        "id": 2,
        "title": "Which framework is better for backend?",
        "date_posted": "may 12, 2006",
        "author": "Mike",
        "content": "eodjakdasjdkadkjaskjdkjasjdka",
    },
    {
        "id": 3,
        "title": "is Python the best programming language?",
        "date_posted": "jun 7, 2012",
        "author": "Nick",
        "content": "eodjakdasjdkadkjaskjdkjasjdka",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    context = {"posts": posts, "title": "Home"}
    return templates.TemplateResponse(request, "home.html", context=context)


@app.get("/post/{post_id}", include_in_schema=False, name="post")
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            context = {
                "post": post,
                "title": post["title"][:50],
            }
            return templates.TemplateResponse(request, "post.html", context=context)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get("/api/posts")
def get_posts():
    return posts


@app.get("/api/post/{post_id}")
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occured. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code, content={"detail": message}
        )

    return templates.TemplateResponse(
        request,
        "error.html",
        context={
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        context={
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
