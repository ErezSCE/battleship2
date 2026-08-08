"""In‑memory store for Battleship games.

The store is a simple module‑level dictionary that lives for the lifetime of the
process. It maps a ``game_id`` (string) to a dictionary containing the game
state. For the current feature we only need to keep the list of ship placements
per game.

In a real application this would be replaced by a database or a more robust
state‑management service.
"""

from typing import Dict, List
from .validation import ShipPlacement

# Structure: {game_id: {"ships": List[ShipPlacement]}}
GAME_STORE: Dict[str, Dict[str, List[ShipPlacement]]] = {}
