from fastapi import FastAPI

from routers import business
from routers import admin
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# app.include_router(user.router, prefix="/user")
app.include_router(business.router, prefix="/api")
app.include_router(admin.router, prefix="/admin")
