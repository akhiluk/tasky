from fastapi import FastAPI
from tasky.routers import users, auth, tasks, lists
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(lists.router)
app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)

origins = ['*']

app.add_middleware(CORSMiddleware, allow_origins = origins, allow_credentials = True, allow_methods = ['*'], allow_headers = ['*'])