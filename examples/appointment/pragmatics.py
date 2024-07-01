from examples.appointment.ontology import *


def is_relevant_answer(move, question):
    if isinstance(question, WhQuestion):
        if isinstance(move, ShortAnswer) and move.individual.sort == question.predicate.sort:
            return True
