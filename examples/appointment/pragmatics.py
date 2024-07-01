from examples.appointment.ontology import *


def is_relevant_answer(move, question):
    if isinstance(question, WhQuestion):
        if isinstance(move, ShortAnswer) and move.individual.sort == question.predicate.sort:
            return True
    if isinstance(question, BooleanQuestion):
        if isinstance(move, Confirm):
            return True


def combine(move, question):
    if isinstance(question, WhQuestion):
        if isinstance(move, ShortAnswer) and move.individual.sort == question.predicate.sort:
            return PredicateProposition(question.predicate, move.individual)
    if isinstance(question, BooleanQuestion):
        if isinstance(move, Confirm):
            return PredicateProposition(question.predicate, True)
