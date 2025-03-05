from abc import ABC
from dataclasses import dataclass
from enum import Enum


class Classification(ABC):
    pass


class DiscStability(Enum):
    VERY_UNDERSTABLE = "Very Understable"
    UNDERSTABLE = "Understable"
    STABLE = "Stable"
    OVERSTABLE = "Overstable"
    VERY_OVERSTABLE = "Very Overstable"


class PlayerClassification(Enum):
    PROFESSIONAL = "Professional"
    AMATEUR = "Amateur"


@dataclass
class Disc:
    id: int
    name: str
    manufacturer: str
    type: str
    speed: int
    glide: int
    turn: int
    fade: int

@dataclass
class Course:
    id: int
    name: str
    location: str
    holes: int
    country: str
    city: str

@dataclass
class Score:
    id: int
    player_name: str
    course_id: int
    total_score: int
    date_played: str

@dataclass
class Player:
    id: int
    name: str
    first_name: str
    last_name: str
    pdga_number: int
    location: str
    classification: str
    member_since: int
    career_events: int
    career_wins: int
    carrer_earnings: float
    rating: int
    division: str
    last_update: int


