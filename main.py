from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import Base, engine
from error_handlers import general_http_exception_handler, validation_exception_handler
from posts.pages import router as posts_pages
from posts.routers import router as posts_router
from users.pages import router as users_pages
from users.routers import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts_router)
app.include_router(posts_pages)
app.include_router(users_router)
app.include_router(users_pages)


app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory="media"), name="media")


app.add_exception_handler(StarletteHTTPException, general_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
