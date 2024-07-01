from isupy.ontology import *
import isupy.ontology


def Sort(name):
    return TypeVar(name, bound=SemanticType)


def Individual(name, sort):
    return TypeVar(name, bound=sort)


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


@dataclass
class ShortAnswer(Move):
    individual: Individual


Person = Sort('Person')
MeetingDate = Sort('MeetingDate')
Vlad = Individual('Vlad', Person)


@dataclass
class Proposition(SemanticClass):
    pass


@dataclass
class MeetingPerson(Proposition):
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
