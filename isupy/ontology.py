from __future__ import annotations
from typing import TypeVar
from dataclasses import dataclass, field


SemanticType = TypeVar('SemanticClass')


class SemanticClass:
    pass


@dataclass
class Move(SemanticClass):
    pass


@dataclass
class Greet(Move):
    pass


@dataclass
class DialogState:
    latest_moves: list[Move] = field(default_factory=list)
    next_moves: list[Move] = field(default_factory=list)
