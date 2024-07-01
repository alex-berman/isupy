from isupy.rule import Rule
from isupy.isu import try_rule
import isupy.dm
from isupy.logger import logger

from examples.appointment.ontology import *
from examples.appointment.pragmatics import is_relevant_answer


class DialogueManager(isupy.dm.DialogueManager):
    @staticmethod
    def get_next_moves(state: DialogState):
        logger.debug('get_next_moves')
        state.next_moves = []
        try_rule(state, SelectNegativeUnderstanding)
        try_rule(state, IntegrateRequest)
        try_rule(state, IntegrateShortAnswer)
        try_rule(state, SelectGreet)
        try_rule(state, SelectAsk)
        logger.debug('get_next_moves returns', next_moves=state.next_moves)
        return state.next_moves

    @staticmethod
    def set_latest_moves(state: DialogState, moves):
        state.latest_moves = moves


class SelectGreet(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.agenda) > 0 and state.agenda[0] == GreetAction()

    @staticmethod
    def effects(state: DialogState):
        state.agenda.pop(0)
        state.next_moves.append(Greet())


class SelectAsk(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.agenda) > 0 and isinstance(state.agenda[0], Findout)

    @staticmethod
    def effects(state: DialogState):
        state.next_moves.append(Ask(state.agenda[0].question))


class IntegrateRequest(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.latest_moves) > 0 and state.latest_moves[0] == Request(CreateAppointment())

    @staticmethod
    def effects(state: DialogState):
        state.agenda = [
            Findout(WhQuestion(meeting_person)),
            Findout(WhQuestion(meeting_date)),
            Findout(BooleanQuestion(meeting_whole_day))
            ] + state.agenda


class IntegrateShortAnswer(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        if len(state.agenda) > 0:
            current_action = state.agenda[0]
            if isinstance(current_action, Findout):
                current_question = current_action.question
                for move in state.latest_moves:
                    if is_relevant_answer(move, current_question):
                        return {'predicate': current_question.predicate, 'individual': move.individual}

    @staticmethod
    def effects(state: DialogState, predicate, individual):
        state.agenda.pop(0)
        state.facts.append(PredicateProposition(predicate, individual))


class SelectNegativeUnderstanding(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        if len(state.agenda) > 0 and len(state.latest_moves) > 0:
            current_action = state.agenda[0]
            if isinstance(current_action, Findout):
                current_question = current_action.question
                if not any(is_relevant_answer(move, current_question) for move in state.latest_moves):
                    return True

    @staticmethod
    def effects(state: DialogState):
        state.next_moves.insert(0, NegativeUnderstanding())
