from examples.appointment.ontology import *


def is_relevant_answer(move, question):
    if isinstance(question, WhQuestion):
        if isinstance(move, ShortAnswer) and move.individual.sort == question.predicate.sort:
            return True
        if isinstance(move, PropositionalAnswer) and move.predicate == question.predicate:
            return True
    if isinstance(question, BooleanQuestion):
        if isinstance(move, (Confirm, Deny)):
            return True
        if isinstance(move, PropositionalAnswer) and move.predicate == question.predicate:
            return True


def combine(move, question):
    if isinstance(question, WhQuestion):
        if isinstance(move, ShortAnswer) and move.individual.sort == question.predicate.sort:
            return PredicateProposition(question.predicate, move.individual)
        if isinstance(move, PropositionalAnswer) and move.predicate == question.predicate:
            return PredicateProposition(question.predicate, move.argument)
    if isinstance(question, BooleanQuestion):
        if isinstance(move, Confirm):
            return PredicateProposition(question.predicate, True)
        if isinstance(move, Deny):
            return PredicateProposition(question.predicate, False)
        if isinstance(move, PropositionalAnswer) and move.predicate == question.predicate:
            return PredicateProposition(question.predicate, move.argument)
