from fastapi import FastAPI


app = FastAPI(title="Battleship API")

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
