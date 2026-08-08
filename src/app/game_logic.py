"""Game logic utilities for Battleship backend.

This module provides functions to handle shot processing, hit detection,
ship sinking, and win condition evaluation. The in‑memory store keeps a
`board` entry per game, which is a list of ship dictionaries with the
following structure:

```python
{
    "positions": [(x1, y1), (x2, y2), ...],  # coordinates occupied by the ship
    "hits": []  # coordinates that have been hit so far
}
```

The functions mutate the board in‑place and return a result string that
matches the `ShotResultResponse` model.
"""
from typing import List, Tuple, Dict

Ship = Dict[str, List[Tuple[int, int]]]

def _find_ship(board: List[Ship], x: int, y: int):
    """Return the ship dict that occupies (x, y) or None.
    """
    for ship in board:
        if (x, y) in ship.get("positions", []):
            return ship
    return None

def process_shot(board: List[Ship], x: int, y: int) -> str:
    """Process a shot at coordinates (x, y).

    Returns one of "miss", "hit", "sunk", or "win".
    The board is mutated: hits are recorded, and sunk ships are left
    unchanged (hits list grows).
    """
    ship = _find_ship(board, x, y)
    if not ship:
        return "miss"
    # Record hit if not already recorded
    if (x, y) not in ship.get("hits", []):
        ship.setdefault("hits", []).append((x, y))
    # Determine if ship is now sunk
    if set(ship["hits"]) == set(ship["positions"]):
        # Check if all ships are sunk for win condition
        all_sunk = all(set(s.get("hits", [])) == set(s.get("positions", [])) for s in board)
        return "win" if all_sunk else "sunk"
    return "hit"
