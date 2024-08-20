from isupy.isu import repeat_until_none_applicable
import isupy.dm
from isupy.logger import logger

from examples.appointment.ontology import *
from examples.appointment.pragmatics import is_relevant_answer, combine
from examples.appointment.plans import plans


def get_fact_argument(state, predicate):
    for fact in state.facts:
        if isinstance(fact, PredicateProposition) and fact.predicate == predicate:
            return fact.argument


class DialogueManager(isupy.dm.DialogueManager):
    @staticmethod
    def get_next_moves(state: DialogState):
        logger.debug('get_next_moves')
        state.next_moves = []
        state.non_processed_moves = list(state.latest_moves)
        repeat_until_none_applicable(state, [
            integrate_request,
            integrate_answer_for_findout,
            integrate_short_answer_for_confirm_action,
            select_greet,
            select_negative_understanding,
            select_ask_via_findout,
            select_ask_action_confirmation,
            execute_function
        ])
        logger.debug('get_next_moves returns', next_moves=state.next_moves)
        return state.next_moves

    @staticmethod
    def set_latest_moves(state: DialogState, moves):
        state.latest_moves = moves


def select_greet(state: DialogState):
    if len(state.agenda) > 0 and state.agenda[0] == GreetAction():
        yield True
        state.agenda.pop(0)
        state.next_moves.append(Greet())


def select_ask_via_findout(state: DialogState):
    if len(state.non_processed_moves) == 0 and len(state.agenda) > 0 and isinstance(state.agenda[0], Findout) and \
            not any(isinstance(move, Ask) for move in state.next_moves):
        question = state.agenda[0].question
        if question not in state.resolved_questions:
            yield True
            state.next_moves.append(Ask(question))


def select_ask_action_confirmation(state: DialogState):
    if len(state.agenda) > 0 and isinstance(state.agenda[0], PerformAction) and not any(
            isinstance(move, Ask) for move in state.next_moves):
        yield True
        perform_action = state.agenda[0]
        parameters = [
            PredicateProposition(predicate, get_fact_argument(state, predicate))
            for predicate in perform_action.predicates
        ]
        state.next_moves.append(Ask(ActionConfirmation(perform_action.action, parameters)))


def integrate_request(state: DialogState):
    if len(state.non_processed_moves) > 0 and isinstance(state.non_processed_moves[0], Request):
        action_class = state.non_processed_moves[0].action.__class__
        if action_class in plans:
            yield True
            plan = plans[action_class]
            state.agenda = plan + state.agenda
            state.non_processed_moves.pop(0)


def integrate_answer_for_findout(state: DialogState):
    if len(state.agenda) > 0:
        current_action = state.agenda[0]
        if isinstance(current_action, Findout):
            current_question = current_action.question
            for move in state.non_processed_moves:
                if is_relevant_answer(move, current_question):
                    yield True
                    state.agenda.pop(0)
                    state.facts.append(combine(move, current_question))
                    state.non_processed_moves.remove(move)
                    state.resolved_questions.append(current_question)


def integrate_short_answer_for_confirm_action(state: DialogState):
    if len(state.agenda) > 0:
        current_action = state.agenda[0]
        if isinstance(current_action, PerformAction):
            for move in state.non_processed_moves:
                if move in [Confirm(), Deny()]:
                    yield True
                    if move == Confirm():
                        state.next_moves.insert(0, PerformedAction(state.agenda[0].action))
                        state.agenda.pop(0)
                        state.non_processed_moves.remove(move)
                    else:
                        on_deny = state.agenda[0].on_deny
                        state.agenda.pop(0)
                        state.non_processed_moves.remove(move)
                        if on_deny:
                            on_deny()


def select_negative_understanding(state: DialogState):
    if len(state.agenda) > 0 and len(state.non_processed_moves) > 0 and \
            NegativeUnderstanding() not in state.next_moves:
        current_action = state.agenda[0]
        if isinstance(current_action, Findout):
            current_question = current_action.question
            if not any(is_relevant_answer(move, current_question) for move in state.non_processed_moves):
                yield True
                state.next_moves.insert(0, NegativeUnderstanding())
                state.non_processed_moves = []


def execute_function(state: DialogState):
    if len(state.agenda) > 0 and isinstance(state.agenda[0], ExecuteFunction):
        yield True
        function = state.agenda.pop(0).function
        function(state)

