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
boolean = create_sort('boolean')
meeting_person = Predicate(person)
meeting_date = Predicate(date)
meeting_whole_day = Predicate(boolean)
vlad = Individual('vlad', person)
monday = Individual('monday', date)


@dataclass
class Action(SemanticClass):
    pass


@dataclass
class GreetAction(Action):
    pass


@dataclass
class Proposition(SemanticClass):
    pass


@dataclass
class PredicateProposition(Proposition):
    predicate: Predicate
    argument: Individual


@dataclass
class CreateWholeDayMeeting(Proposition):
    pass


@dataclass
class ActionConfirmation(Proposition):
    action: SemanticClass
    parameters: list[Proposition]


@dataclass
class Question(SemanticClass):
    pass


@dataclass
class WhQuestion(Question):
    predicate: Predicate


@dataclass
class BooleanQuestion(Question):
    predicate: Predicate


@dataclass
class Findout(Action):
    question: Question


@dataclass
class ConfirmAction(Action):
    action: SemanticClass
    predicates: list[Predicate]


@dataclass
class Ask(Move):
    question: Question


@dataclass
class ShortAnswer(Move):
    individual: Individual


@dataclass
class Request(Move):
    action: Action


@dataclass
class Confirm(Move):
    pass


@dataclass
class PerformedAction(Move):
    action: SemanticClass


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
