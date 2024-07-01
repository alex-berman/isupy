from isupy.ontology import *
import isupy.ontology


@dataclass
class Action:
    pass


@dataclass
class GreetAction(Action):
    pass


@dataclass
class Private:
    agenda: list[Action] = field(default_factory=lambda: [GreetAction()])


@dataclass
class DialogState(isupy.ontology.DialogState):
    private: Private = field(default_factory=Private)
