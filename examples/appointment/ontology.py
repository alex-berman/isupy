from isupy.ontology import *
import isupy.ontology


@dataclass
class Action(SemanticClass):
    pass


@dataclass
class GreetAction(Action):
    pass


@dataclass
class Findout(Action):
    predicate: SemanticClass


@dataclass
class Question(SemanticClass):
    pass


@dataclass
class WhQuestion(Question):
    predicate: SemanticClass


@dataclass
class Ask(Move):
    question: Question


def Sort(name):
    return TypeVar(name, bound=SemanticType)


def Individual(name, sort):
    return TypeVar(name, bound=sort)


Person = Sort('Person')


@dataclass
class Proposition(SemanticClass):
    pass


@dataclass
class Who(Proposition):
    person: Person


@dataclass
class Request(Move):
    action: Action


@dataclass
class CreateAppointment(Action):
    pass


@dataclass
class Private:
    agenda: list[Action] = field(default_factory=lambda: [GreetAction()])


@dataclass
class DialogState(isupy.ontology.DialogState):
    private: Private = field(default_factory=Private)
