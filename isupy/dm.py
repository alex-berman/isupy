from abc import ABC, abstractmethod

from isupy.ontology import DialogState


class DialogueManager(ABC):
    @staticmethod
    @abstractmethod
    def get_next_moves(state: DialogState):
        pass

    @staticmethod
    @abstractmethod
    def set_latest_moves(state: DialogState):
        pass
