from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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
        "date_posted": "jun 7, 2012",
        "author": "Nick",
        "content": "eodjakdasjdkadkjaskjdkjasjdka",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    context = {"posts": posts}
    return templates.TemplateResponse(request, "home.html", context=context)


@app.get("/api/posts")
def get_posts():
    return posts
