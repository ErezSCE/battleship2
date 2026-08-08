from pydantic import BaseModel

class ShotRequest(BaseModel):
    shooter_id: str
    target_x: int
    target_y: int

class ShotResultResponse(BaseModel):
    result: str  # Expected values: "hit", "miss", "sunk", "win"
