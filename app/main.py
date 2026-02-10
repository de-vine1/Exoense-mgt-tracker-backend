from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import student_router, parent_router, admin_router, auth_router

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth_router.router, prefix=settings.API_V1_STR)
app.include_router(student_router.router, prefix=settings.API_V1_STR)
app.include_router(parent_router.router, prefix=settings.API_V1_STR)
app.include_router(admin_router.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Wallet API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
