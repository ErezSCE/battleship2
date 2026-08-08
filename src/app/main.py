from fastapi import FastAPI, HTTPException
from .models import ShotRequest, ShotResultResponse
from .game_logic import process_shot
from pydantic import BaseModel
import uuid

app = FastAPI(title="Battleship API")

# In-memory store for games
# Structure: {game_id: {"board": [], "current_turn": "player1", "players": ["player1", "player2"]}}
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
    _game_store[game_id] = {"board": [], "current_turn": "player1", "players": []}
    return GameCreateResponse(game_id=game_id)

@app.post("/games/{game_id}/shots", response_model=ShotResultResponse)
async def fire_shot(game_id: str, shot: ShotRequest):
    """Process a shot for a given game.

    Validates the game exists, then uses the game_logic.process_shot function to determine the result.
    Returns a ShotResultResponse containing the result string ("hit", "miss", "sunk", or "win").
    """
    if game_id not in _game_store:
        raise HTTPException(status_code=404, detail="Game not found")
    board = _game_store[game_id]["board"]
    result = process_shot(board, shot.target_x, shot.target_y)
    return ShotResultResponse(result=result)
