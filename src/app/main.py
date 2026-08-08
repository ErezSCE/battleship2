from fastapi import FastAPI, HTTPException
from fastapi import Path
from typing import List

from .validation import ShipPlacement, validate_ship_placements
from .store import GAME_STORE

app = FastAPI(title="Battleship API")

@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

@app.post("/games/{game_id}/ships")
async def place_ships(
    game_id: str = Path(..., description="Identifier of the game"),
    placements: List[ShipPlacement] = None,
):
    """Endpoint to place ships for a given game.

    The request body must be a JSON array of ship placement objects. The
    ``validate_ship_placements`` function enforces the business rules. On success
    the placements are stored in the in‑memory ``GAME_STORE`` under the provided
    ``game_id``.
    """
    if placements is None:
        raise HTTPException(status_code=400, detail="request body must be a list of ship placements")
    # Validate placements according to game rules
    validate_ship_placements(placements)

    # Store placements – create game entry if it does not exist yet
    if game_id not in GAME_STORE:
        GAME_STORE[game_id] = {"ships": []}
    GAME_STORE[game_id]["ships"] = placements
    return {"status": "ships placed", "game_id": game_id}
