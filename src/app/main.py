from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI(title="Battleship API")

# In-memory store for games
# Structure: {game_id: {"board": [], "current_turn": "player1"}}
_game_store: dict[str, dict] = {}

class GameCreateResponse(BaseModel):
    game_id: str

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

@app.post("/games", status_code=201, response_model=GameCreateResponse)
async def create_game():
    """Create a new game session and return its unique identifier.

    Generates a UUID for the game, stores an initial empty board state with the turn set to player1,
    and returns the identifier.
    """
    game_id = str(uuid.uuid4())
    # Initialize empty board and turn information
    _game_store[game_id] = {"board": [], "current_turn": "player1"}
    return GameCreateResponse(game_id=game_id)
