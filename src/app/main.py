from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Battleship API")

@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
