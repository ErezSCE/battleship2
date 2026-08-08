# QA Lead — Test Plan

**Agent**: qa-lead  
**Generated**: 2026-08-08T09:20:29.560Z

---

## Test Plan

{
  "scope": "No explicit user stories or acceptance criteria were supplied. This test plan targets the core functionality described in the architecture: game creation, ship placement, firing shots, board queries, and the main user flows in the Angular UI.",
  "unit": [
    {
      "target": "backend/services/game_service.py::create_game",
      "description": "Verify that a new game object is created with correct initial state and stored in the in‑memory store.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "target": "backend/services/game_service.py::place_ship",
      "description": "Validate ship placement logic: correct orientation, bounds checking, no overlap, and ship state is marked as placed.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "target": "backend/services/game_service.py::fire_shot",
      "description": "Ensure shot handling records hit/miss, updates ship health, and toggles turn correctly.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "target": "backend/services/game_service.py::check_winner",
      "description": "Confirm that the winner detection returns the correct player when all opponent ships are sunk.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "target": "backend/models/board.py::Board.validate_coordinates",
      "description": "Unit test coordinate validation for out‑of‑bounds and negative values.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "target": "backend/models/ship.py::Ship.calculate_occupied_cells",
      "description": "Verify that a ship's occupied cells are correctly calculated based on start position, size, and orientation.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    }
  ],
  "integration": [
    {
      "target": "POST /games",
      "description": "Integration test that creating a game via the API returns 201, a gameId, and initializes the game state in the store.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "target": "POST /games/{game_id}/players",
      "description": "Test adding a player to a game; response includes playerId and updates game player list.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "target": "POST /games/{game_id}/place_ship",
      "description": "Validate that a valid ship placement request updates the store and returns success; invalid placements return 400.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "target": "POST /games/{game_id}/fire",
      "description": "Ensure firing a shot via the endpoint records the shot, returns hit/miss status, and switches turn.",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "target": "GET /games/{game_id}/board?player_id={player_id}",
      "description": "Confirm that board query returns the correct visible grid for the requesting player (own ships visible, opponent ships hidden).",
      "framework": "pytest",
      "storyId": "N/A",
      "acIndex": -1
    }
  ],
  "e2e": [
    {
      "scenario": "User creates a new game and is taken to the ship placement screen.",
      "description": "End‑to‑end flow verifies that the UI can start a game, receives a gameId, and displays an empty board ready for placement.",
      "criticalPath": true,
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "scenario": "User places all required ships without overlap and proceeds to the firing phase.",
      "description": "E2E test checks drag‑and‑drop or form submission for each ship, validates backend acceptance, and UI transition to opponent view.",
      "criticalPath": true,
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "scenario": "User fires a shot, sees hit/miss feedback, and turn switches to opponent.",
      "description": "Simulates a shot request, asserts that the UI updates the cell color, and that the next turn indicator changes.",
      "criticalPath": true,
      "storyId": "N/A",
      "acIndex": -1
    },
    {
      "scenario": "User sinks all opponent ships and the victory screen is displayed.",
      "description": "Full game playthrough until win condition; verifies that the backend reports winner and UI shows congratulatory message.",
      "criticalPath": true,
      "storyId": "N/A",
      "acIndex": -1
    }
  ],
  "coverageTargets": {
    "unit": 85,
    "integration": 70,
    "e2e": 100
  }
}
