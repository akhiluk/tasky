from fastapi import FastAPI
from tasky.routers import users, auth, tasks, lists
# from tasky.config import settings

app = FastAPI()

app.include_router(lists.router)
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)