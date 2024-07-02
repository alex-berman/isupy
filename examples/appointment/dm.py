from isupy.rule import Rule
from isupy.isu import repeat_until_none_applicable, try_rule
import isupy.dm
from isupy.logger import logger

from examples.appointment.ontology import *
from examples.appointment.pragmatics import is_relevant_answer, combine


def get_fact_argument(state, predicate):
    for fact in state.facts:
        if isinstance(fact, PredicateProposition) and fact.predicate == predicate:
            return fact.argument


class DialogueManager(isupy.dm.DialogueManager):
    @staticmethod
    def get_next_moves(state: DialogState):
        logger.debug('get_next_moves')
        state.next_moves = []
        state.non_integrated_moves = list(state.latest_moves)
        repeat_until_none_applicable(state, [
            SelectNegativeUnderstanding,
            IntegrateRequest,
            IntegrateShortAnswerForFindout,
            SelectGreet,
            SelectAskViaFindout,
            IntegrateShortAnswerForConfirmAction,
            SelectAskActionConfirmation,
            ExecTryRule
        ])
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


class SelectAskViaFindout(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.agenda) > 0 and isinstance(state.agenda[0], Findout) and \
               Ask(state.agenda[0].question) not in state.next_moves

    @staticmethod
    def effects(state: DialogState):
        state.next_moves.append(Ask(state.agenda[0].question))


class SelectAskActionConfirmation(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.agenda) > 0 and isinstance(state.agenda[0], PerformAction) and not any(
            isinstance(move, Ask) for move in state.next_moves
        )

    @staticmethod
    def effects(state: DialogState):
        perform_action = state.agenda[0]
        parameters = [
            PredicateProposition(predicate, get_fact_argument(state, predicate))
            for predicate in perform_action.predicates
        ]
        state.next_moves.append(Ask(ActionConfirmation(perform_action.action, parameters)))


class IntegrateRequest(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.non_integrated_moves) > 0 and state.non_integrated_moves[0] == Request(CreateAppointment())

    @staticmethod
    def effects(state: DialogState):
        state.agenda = [
            Findout(WhQuestion(meeting_person)),
            Findout(WhQuestion(meeting_date)),
            Findout(BooleanQuestion(meeting_whole_day)),
            TryRule(PlanActionsDependingOnMeetingWholeDay)
            ] + state.agenda
        state.non_integrated_moves.pop(0)


class PlanActionsDependingOnMeetingWholeDay(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return True

    @staticmethod
    def effects(state: DialogState):
        if PredicateProposition(meeting_whole_day, True) in state.facts:
            state.agenda.insert(0, PerformAction(CreateWholeDayMeeting, [meeting_person, meeting_date]))
        else:
            state.agenda = [
                Findout(WhQuestion(meeting_time)),
                PerformAction(CreateNotWholeDayMeeting, [meeting_person, meeting_date, meeting_time])
            ] + state.agenda


class IntegrateShortAnswerForFindout(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        if len(state.agenda) > 0:
            current_action = state.agenda[0]
            if isinstance(current_action, Findout):
                current_question = current_action.question
                for move in state.non_integrated_moves:
                    if is_relevant_answer(move, current_question):
                        return {'move': move, 'question': current_question}

    @staticmethod
    def effects(state: DialogState, move, question):
        state.agenda.pop(0)
        state.facts.append(combine(move, question))
        state.non_integrated_moves.remove(move)


class IntegrateShortAnswerForConfirmAction(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        if len(state.agenda) > 0:
            current_action = state.agenda[0]
            if isinstance(current_action, PerformAction):
                for move in state.non_integrated_moves:
                    if isinstance(move, Confirm):
                        return {'move': move}

    @staticmethod
    def effects(state: DialogState, move):
        state.next_moves.insert(0, PerformedAction(state.agenda[0].action))
        state.agenda.pop(0)
        state.non_integrated_moves.remove(move)


class SelectNegativeUnderstanding(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        if len(state.agenda) > 0 and len(state.non_integrated_moves) > 0 and \
                NegativeUnderstanding() not in state.next_moves:
            current_action = state.agenda[0]
            if isinstance(current_action, Findout):
                current_question = current_action.question
                if not any(is_relevant_answer(move, current_question) for move in state.non_integrated_moves):
                    return True

    @staticmethod
    def effects(state: DialogState):
        state.next_moves.insert(0, NegativeUnderstanding())


class ExecTryRule(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.agenda) > 0 and isinstance(state.agenda[0], TryRule)

    @staticmethod
    def effects(state: DialogState):
        rule = state.agenda.pop(0).rule
        try_rule(state, rule)
