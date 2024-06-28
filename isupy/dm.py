from abc import ABC, abstractmethod

from isupy.ontology import DialogState


class DialogueManager(ABC):
    @staticmethod
    @abstractmethod
    def get_system_move(state: DialogState):
        pass

    @staticmethod
    @abstractmethod
    def set_user_move(state: DialogState):
        pass
