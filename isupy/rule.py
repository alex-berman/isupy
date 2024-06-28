from abc import ABC, abstractmethod

from isupy.ontology import DialogState


class Rule(ABC):
    @staticmethod
    @abstractmethod
    def preconditions(state: DialogState):
        pass

    @staticmethod
    @abstractmethod
    def effects(state: DialogState):
        pass
