import pytest
import uuid
from httpx import AsyncClient
from src.app.main import app, _game_store

@pytest.mark.asyncio
async def test_create_game_returns_uuid_and_stores_state():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post("/games")
    assert response.status_code == 201
    data = response.json()
    assert "game_id" in data
    # Validate UUID format
    try:
        uuid_obj = uuid.UUID(data["game_id"], version=4)
    except Exception as e:
        pytest.fail(f"game_id is not a valid UUID: {e}")
    # Ensure game is stored with correct initial state
    game_id = data["game_id"]
    assert game_id in _game_store
    stored = _game_store[game_id]
    assert stored["board"] == []
    assert stored["current_turn"] == "player1"

@pytest.mark.asyncio
async def test_multiple_game_creations_yield_distinct_ids():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        resp1 = await client.post("/games")
        resp2 = await client.post("/games")
    id1 = resp1.json()["game_id"]
    id2 = resp2.json()["game_id"]
    assert id1 != id2
