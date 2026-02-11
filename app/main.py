from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import routers
from app.api.auth.router import router as auth_router

app = FastAPI(title=settings.APP_NAME)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend URLS
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Include Routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(routers.student_router, prefix=f"{settings.API_V1_STR}/students", tags=["Students"])
app.include_router(routers.parent_router, prefix=f"{settings.API_V1_STR}/parents", tags=["Parents"])
app.include_router(routers.staff_router, prefix=f"{settings.API_V1_STR}/staff", tags=["Staff"])
app.include_router(routers.product_router, prefix=f"{settings.API_V1_STR}/products", tags=["Products"])
app.include_router(routers.wallet_router, prefix=f"{settings.API_V1_STR}/wallets", tags=["Wallets"])
app.include_router(routers.sale_router, prefix=f"{settings.API_V1_STR}/sales", tags=["Sales"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Wallet API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
