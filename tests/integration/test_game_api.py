import pytest
import uuid
from fastapi.testclient import TestClient
from src.app.main import app, _game_store

client = TestClient(app)

@pytest.fixture
def new_game_id():
    """Create a new game and return its ID for use in subsequent tests."""
    response = client.post("/games")
    assert response.status_code == 201
    return response.json()["game_id"]

def test_post_players_adds_player(new_game_id):
    """Integration test that adding a player to a game returns a playerId and updates the game state.
    Expected behavior per test plan: 200 OK with playerId in response and game store updated.
    """
    payload = {"player_name": "Alice"}
    response = client.post(f"/games/{new_game_id}/players", json=payload)
    # The endpoint is not implemented in the current codebase; expecting failure.
    assert response.status_code == 200
    data = response.json()
    assert "player_id" in data
    # Verify store update (hypothetical structure)
    assert "players" in _game_store[new_game_id]
    assert any(p["id"] == data["player_id"] for p in _game_store[new_game_id]["players"])

def test_place_ship_success(new_game_id):
    """Validate that a valid ship placement updates the store and returns success.
    Expected: 200 OK with confirmation.
    """
    payload = {
        "player_id": "player1",
        "ship_type": "destroyer",
        "start": [0, 0],
        "orientation": "horizontal",
    }
    response = client.post(f"/games/{new_game_id}/place_ship", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "success"

def test_fire_shot_success(new_game_id):
    """Ensure firing a shot records it and returns hit/miss status.
    Expected: 200 OK with result.
    """
    payload = {"player_id": "player1", "target": [0, 0]}
    response = client.post(f"/games/{new_game_id}/fire", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("result") in {"hit", "miss"}

def test_get_board_visibility(new_game_id):
    """Confirm board query returns correct visible grid for the player.
    Expected: 200 OK with board data.
    """
    player_id = "player1"
    response = client.get(f"/games/{new_game_id}/board", params={"player_id": player_id})
    assert response.status_code == 200
    data = response.json()
    assert "grid" in data
