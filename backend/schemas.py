from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class PlayerBase(BaseModel):
    player_name: str = Field(min_length = 2, max_length = 50)
    player_number: int = Field(ge = 1, le=99)
    position: Literal["GK", "DEF", "MID", "FWD"]

class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    on_starting_xi: bool
    model_config = ConfigDict(from_attributes=True)