from enum import Enum
from typing import List, Optional

from beanie import Document
from pydantic import BaseModel, ConfigDict


class RacketSponsor(str, Enum):
    DUNLOP = "Dunlop"
    TECNIFIBRE = "Tecnifibre"
    HEAD = "Head"
    UNSQUASHABLE = "Unsquashable"
    VICTOR = "Victor"
    PRINCE = "Prince"


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class PlayerStats(BaseModel):
    matches_played: int
    matches_won: int
    career_titles: int


class MatchRecord(BaseModel):
    date: str
    tournament: str
    opponent: str
    result: str
    score: str


class Player(Document):
    model_config = ConfigDict(validate_assignment=True)
    name: str
    gender: Gender
    country: str
    current_rank: Optional[int] = None
    status: Optional[str] = "Active"
    plays: str
    racket_sponsor: RacketSponsor
    bio: str
    stats: PlayerStats
    recent_matches: List[MatchRecord] = []

    class Settings:
        name = "squash"
        validate_on_save = True
