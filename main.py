from fastapi import FastAPI

from routers import business, user, admin

app = FastAPI()

app.include_router(user.router, prefix="/user")
app.include_router(business.router, prefix="/api")
app.include_router(admin.router, prefix="/admin")
