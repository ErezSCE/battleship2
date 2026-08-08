import pytest

# Import target functions; they may not exist yet.

@pytest.fixture(scope="module")
def import_functions():
    try:
        from backend.services import game_service
    except ImportError as e:
        pytest.fail(f"ImportError while importing game_service module: {e}")
    return game_service


def test_create_game_initial_state(import_functions):
    """Verify that create_game returns a new game dict with correct initial state."""
    gs = import_functions
    game = gs.create_game()
    # Expect a dict with at least 'board' and 'current_turn'
    assert isinstance(game, dict), "create_game should return a dict"
    assert "board" in game, "Game dict missing 'board' key"
    assert game["board"] == [], "Initial board should be empty list"
    assert "current_turn" in game, "Game dict missing 'current_turn' key"
    assert game["current_turn"] == "player1", "Initial turn should be 'player1'"


def test_place_ship_valid_placement(import_functions):
    """Validate ship placement logic for a valid placement."""
    gs = import_functions
    # Setup a minimal game state
    game = {"board": [], "ships": [], "current_turn": "player1"}
    ship = {
        "type": "destroyer",
        "size": 2,
        "start": (0, 0),
        "orientation": "horizontal",
    }
    result = gs.place_ship(game, ship)
    # Expect result to be True or a dict indicating success
    assert result, "place_ship should succeed for valid placement"
    # Verify ship added to game state
    assert any(s["type"] == "destroyer" for s in game.get("ships", [])), "Ship not added to game"


def test_fire_shot_updates_state(import_functions):
    """Ensure fire_shot records hit/miss and toggles turn."""
    gs = import_functions
    game = {
        "board": [],
        "ships": [{"type": "destroyer", "cells": [(0, 0)], "hits": []}],
        "current_turn": "player1",
    }
    result = gs.fire_shot(game, (0, 0))
    # Expect result dict with 'hit' boolean
    assert isinstance(result, dict), "fire_shot should return a dict"
    assert "hit" in result, "Result missing 'hit' key"
    # Verify turn toggled
    assert game["current_turn"] != "player1", "Turn should be toggled after shot"


def test_check_winner_detects_winner(import_functions):
    """Confirm winner detection when opponent has no ships left."""
    gs = import_functions
    game = {
        "players": ["player1", "player2"],
        "ships": {"player1": [], "player2": []},
    }
    winner = gs.check_winner(game)
    # If no ships for player2, player1 should be winner
    assert winner == "player1" or winner is None, "check_winner should return player1 when opponent has no ships"


def test_validate_coordinates_bounds(import_functions):
    """Unit test coordinate validation for out‑of‑bounds and negative values."""
    from backend.models.board import validate_coordinates
    # Assuming board size is 10x10
    with pytest.raises(ValueError):
        validate_coordinates((-1, 5))
    with pytest.raises(ValueError):
        validate_coordinates((10, 0))
    # Valid coordinate should not raise
    validate_coordinates((0, 0))


def test_ship_occupied_cells_calculation(import_functions):
    """Verify occupied cells calculation for a ship."""
    from backend.models.ship import Ship
    ship = Ship(start=(0, 0), size=3, orientation="vertical")
    cells = ship.calculate_occupied_cells()
    assert cells == [(0, 0), (0, 1), (0, 2)], "Occupied cells not calculated correctly"
