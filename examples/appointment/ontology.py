from typing import Optional, Callable

from isupy.ontology import *
import isupy.ontology
from isupy.rule import Rule


def create_sort(name):
    return TypeVar(name, bound=SemanticType)


@dataclass
class Individual(SemanticClass):
    name: str
    sort: TypeVar


@dataclass
class Predicate(SemanticClass):
    name: str
    sort: TypeVar


person = create_sort('person')
date = create_sort('date')
time = create_sort('time')
boolean = create_sort('boolean')
meeting_person = Predicate('meeting_person', person)
meeting_date = Predicate('meeting_date', date)
meeting_whole_day = Predicate('meeting_whole_day', boolean)
meeting_time = Predicate('meeting_time', time)
vlad = Individual('vlad', person)
monday = Individual('monday', date)
two_pm = Individual('two_pm', time)


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
class CreateNotWholeDayMeeting(Proposition):
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
class PerformAction(Action):
    action: SemanticClass
    predicates: list[Predicate]
    on_deny: Optional[Callable] = None


@dataclass
class TryRule(Action):
    rule: Rule


@dataclass
class Ask(Move):
    question: Question


@dataclass
class ShortAnswer(Move):
    individual: Individual


@dataclass
class PropositionalAnswer(Move):
    predicate: Predicate
    argument: Individual


@dataclass
class Request(Move):
    action: Action


@dataclass
class Confirm(Move):
    pass


@dataclass
class Deny(Move):
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
    non_processed_moves: list[Move] = field(default_factory=list)
    agenda: list[Action] = field(default_factory=lambda: [GreetAction()])
    facts: list[Proposition] = field(default_factory=list)
    resolved_questions: list[Question] = field(default_factory=list)
