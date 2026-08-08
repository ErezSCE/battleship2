from typing import List, Tuple

from fastapi import HTTPException
from pydantic import BaseModel, validator

BOARD_SIZE = 6

class ShipPlacement(BaseModel):
    """Model representing a single ship placement request.

    Attributes
    ----------
    type: str
        Identifier of the ship type. Expected values are "destroyer", "submarine",
        "battleship" (or any string) – the size is derived from a predefined map.
    orientation: str
        Either "horizontal" or "vertical" (case‑insensitive).
    start_x: int
        Zero‑based column index where the ship starts.
    start_y: int
        Zero‑based row index where the ship starts.
    """

    type: str
    orientation: str
    start_x: int
    start_y: int

    @validator("orientation")
    def orientation_must_be_valid(cls, v: str) -> str:
        if v.lower() not in {"horizontal", "vertical"}:
            raise ValueError("orientation must be 'horizontal' or 'vertical'")
        return v.lower()

    @validator("start_x", "start_y")
    def coordinates_must_be_in_range(cls, v: int) -> int:
        if not (0 <= v < BOARD_SIZE):
            raise ValueError(f"coordinate must be between 0 and {BOARD_SIZE - 1}")
        return v

# Mapping ship type to its length. The story mentions sizes 2, 3, and 4.
SHIP_SIZES = {
    "size2": 2,
    "size3": 3,
    "size4": 4,
    # alternative friendly names could be added here
}

def _ship_cells(placement: ShipPlacement) -> List[Tuple[int, int]]:
    """Return a list of board cells occupied by the ship.

    Parameters
    ----------
    placement: ShipPlacement
        The ship placement description.

    Returns
    -------
    List[Tuple[int, int]]
        List of (x, y) tuples for each cell the ship occupies.
    """
    size = SHIP_SIZES.get(placement.type)
    if size is None:
        raise HTTPException(status_code=400, detail=f"unknown ship type '{placement.type}'")
    cells = []
    if placement.orientation == "horizontal":
        if placement.start_x + size > BOARD_SIZE:
            raise HTTPException(
                status_code=400,
                detail="ship does not fit horizontally on the board",
            )
        for dx in range(size):
            cells.append((placement.start_x + dx, placement.start_y))
    else:  # vertical
        if placement.start_y + size > BOARD_SIZE:
            raise HTTPException(
                status_code=400,
                detail="ship does not fit vertically on the board",
            )
        for dy in range(size):
            cells.append((placement.start_x, placement.start_y + dy))
    return cells


def validate_ship_placements(placements: List[ShipPlacement]) -> None:
    """Validate a collection of ship placements.

    The function enforces three rules required by the user story:
    1. Exactly three ships must be supplied.
    2. Ships must not overlap.
    3. Each ship must fit inside the 6×6 board.

    If any rule is violated an ``HTTPException`` with status code 400 is raised.
    """
    if len(placements) != 3:
        raise HTTPException(status_code=400, detail="exactly three ships must be placed")

    occupied: set[Tuple[int, int]] = set()
    for placement in placements:
        # size validation and out‑of‑bounds are performed inside _ship_cells
        cells = _ship_cells(placement)
        for cell in cells:
            if cell in occupied:
                raise HTTPException(status_code=400, detail="ships may not overlap")
            occupied.add(cell)
