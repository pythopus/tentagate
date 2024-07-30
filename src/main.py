from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import time
from .config import settings
from .auth import get_current_user
from .cache import cache
from .rate_limiter import rate_limiter
from .circuit_breaker import call_backend_service

app = FastAPI(title="TentaGate")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/")
async def root():
    return {"message": "Welcome to TentaGate"}

@app.get("/api/{path:path}")
@cache(expire=60)
async def proxy(
    path: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
    rate_limit: bool = Depends(rate_limiter)
):
    service = path.split("/")[0]
    if service not in settings.BACKEND_SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    backend_url = f"{settings.BACKEND_SERVICES[service]}/{'/'.join(path.split('/')[1:])}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await call_backend_service(
                client,
                method=request.method,
                url=backend_url,
                headers=request.headers,
                params=request.query_params,
                content=await request.body(),
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}