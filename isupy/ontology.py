from __future__ import annotations
from typing import TypeVar
from dataclasses import dataclass


SemanticType = TypeVar('SemanticClass')


class SemanticClass:
    pass


@dataclass
class DialogState:
    pass
