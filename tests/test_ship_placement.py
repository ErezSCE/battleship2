import pytest
from httpx import AsyncClient
from src.app.main import app, GAME_STORE

# Helper to create a valid placement list
valid_placements = [
    {
        "type": "size2",
        "orientation": "horizontal",
        "start_x": 0,
        "start_y": 0,
    },
    {
        "type": "size3",
        "orientation": "vertical",
        "start_x": 2,
        "start_y": 1,
    },
    {
        "type": "size4",
        "orientation": "horizontal",
        "start_x": 1,
        "start_y": 4,
    },
]

@pytest.mark.asyncio
async def test_place_ships_success():
    game_id = "game123"
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(f"/games/{game_id}/ships", json=valid_placements)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["status"] == "ships placed"
    assert json_resp["game_id"] == game_id
    # Verify that the placements are stored in the in‑memory store
    assert game_id in GAME_STORE
    stored = GAME_STORE[game_id]["ships"]
    # stored objects are pydantic models; compare dict representations
    assert [s.dict() for s in stored] == valid_placements

@pytest.mark.asyncio
async def test_place_ships_invalid_count():
    game_id = "game_invalid_count"
    # Only two ships provided
    invalid_payload = valid_placements[:2]
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(f"/games/{game_id}/ships", json=invalid_payload)
    assert response.status_code == 400
    assert "exactly three ships" in response.json()["detail"]

@pytest.mark.asyncio
async def test_place_ships_overlap():
    game_id = "game_overlap"
    # Overlap: first ship occupies (0,0)-(1,0), second ship starts at (1,0) vertically size3
    overlapping = [
        {
            "type": "size2",
            "orientation": "horizontal",
            "start_x": 0,
            "start_y": 0,
        },
        {
            "type": "size3",
            "orientation": "vertical",
            "start_x": 1,
            "start_y": 0,
        },
        {
            "type": "size4",
            "orientation": "horizontal",
            "start_x": 2,
            "start_y": 2,
        },
    ]
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(f"/games/{game_id}/ships", json=overlapping)
    assert response.status_code == 400
    assert "overlap" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_place_ships_out_of_bounds():
    game_id = "game_oob"
    # Ship size4 placed horizontally starting at x=4 (would exceed board size 6)
    oob_payload = [
        {
            "type": "size2",
            "orientation": "horizontal",
            "start_x": 0,
            "start_y": 0,
        },
        {
            "type": "size3",
            "orientation": "vertical",
            "start_x": 2,
            "start_y": 1,
        },
        {
            "type": "size4",
            "orientation": "horizontal",
            "start_x": 4,
            "start_y": 5,
        },
    ]
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post(f"/games/{game_id}/ships", json=oob_payload)
    assert response.status_code == 400
    assert "does not fit" in response.json()["detail"].lower()
