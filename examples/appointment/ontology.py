from isupy.ontology import *
import isupy.ontology


def create_sort(name):
    return TypeVar(name, bound=SemanticType)


@dataclass
class Individual(SemanticClass):
    name: str
    sort: TypeVar


@dataclass
class Predicate(SemanticClass):
    sort: TypeVar


person = create_sort('person')
date = create_sort('date')
meeting_person = Predicate(person)
meeting_date = Predicate(date)
vlad = Individual('vlad', person)
monday = Individual('monday', date)


@dataclass
class Action(SemanticClass):
    pass


@dataclass
class GreetAction(Action):
    pass


@dataclass
class Question(SemanticClass):
    pass


@dataclass
class WhQuestion(Question):
    predicate: TypeVar


@dataclass
class Findout(Action):
    question: Question


@dataclass
class Ask(Move):
    question: Question


@dataclass
class ShortAnswer(Move):
    individual: Individual


@dataclass
class Proposition(SemanticClass):
    pass


@dataclass
class PredicateProposition(SemanticClass):
    predicate: Predicate
    argument: Individual


@dataclass
class Request(Move):
    action: Action


@dataclass
class NegativeUnderstanding(Move):
    pass


@dataclass
class CreateAppointment(Action):
    pass


@dataclass
class DialogState(isupy.ontology.DialogState):
    agenda: list[Action] = field(default_factory=lambda: [GreetAction()])
    facts: list[Proposition] = field(default_factory=list)
