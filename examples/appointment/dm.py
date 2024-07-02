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


def put_appointment_slot_filling_on_agenda(state):
    state.agenda = [
        Findout(WhQuestion(meeting_person)),
        Findout(WhQuestion(meeting_date)),
        Findout(BooleanQuestion(meeting_whole_day)),
        TryRule(PlanActionsDependingOnMeetingWholeDay)
        ] + state.agenda


def forget_and_put_appointment_slot_filling_on_agenda(state):
    state.facts = []
    state.resolved_questions = []
    put_appointment_slot_filling_on_agenda(state)


class DialogueManager(isupy.dm.DialogueManager):
    @staticmethod
    def get_next_moves(state: DialogState):
        logger.debug('get_next_moves')
        state.next_moves = []
        state.non_processed_moves = list(state.latest_moves)
        repeat_until_none_applicable(state, [
            IntegrateRequest,
            IntegrateAnswerForFindout,
            IntegrateShortAnswerForConfirmAction,
            SelectGreet,
            SelectNegativeUnderstanding,
            SelectAskViaFindout,
            SelectAskActionConfirmation,
            ExecTryRule,
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
        if len(state.non_processed_moves) == 0 and len(state.agenda) > 0 and isinstance(state.agenda[0], Findout) and \
                not any(isinstance(move, Ask) for move in state.next_moves):
            question = state.agenda[0].question
            if question not in state.resolved_questions:
                return {'question': question}

    @staticmethod
    def effects(state: DialogState, question: Question):
        state.next_moves.append(Ask(question))


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
        return len(state.non_processed_moves) > 0 and state.non_processed_moves[0] == Request(CreateAppointment())

    @staticmethod
    def effects(state: DialogState):
        put_appointment_slot_filling_on_agenda(state)
        state.non_processed_moves.pop(0)


class PlanActionsDependingOnMeetingWholeDay(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return True

    @staticmethod
    def effects(state: DialogState):
        if PredicateProposition(meeting_whole_day, True) in state.facts:
            state.agenda.insert(
                0, PerformAction(CreateWholeDayMeeting, [meeting_person, meeting_date],
                                 on_deny=lambda: forget_and_put_appointment_slot_filling_on_agenda(state)))
        else:
            state.agenda = [
                Findout(WhQuestion(meeting_time)),
                PerformAction(CreateNotWholeDayMeeting, [meeting_person, meeting_date, meeting_time],
                              on_deny=lambda: forget_and_put_appointment_slot_filling_on_agenda(state))
            ] + state.agenda


class IntegrateAnswerForFindout(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        if len(state.agenda) > 0:
            current_action = state.agenda[0]
            if isinstance(current_action, Findout):
                current_question = current_action.question
                for move in state.non_processed_moves:
                    if is_relevant_answer(move, current_question):
                        return {'move': move, 'question': current_question}

    @staticmethod
    def effects(state: DialogState, move, question):
        state.agenda.pop(0)
        state.facts.append(combine(move, question))
        state.non_processed_moves.remove(move)
        state.resolved_questions.append(question)


class IntegrateShortAnswerForConfirmAction(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        if len(state.agenda) > 0:
            current_action = state.agenda[0]
            if isinstance(current_action, PerformAction):
                for move in state.non_processed_moves:
                    if move in [Confirm(), Deny()]:
                        return {'move': move}

    @staticmethod
    def effects(state: DialogState, move):
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


class SelectNegativeUnderstanding(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        if len(state.agenda) > 0 and len(state.non_processed_moves) > 0 and \
                NegativeUnderstanding() not in state.next_moves:
            current_action = state.agenda[0]
            if isinstance(current_action, Findout):
                current_question = current_action.question
                if not any(is_relevant_answer(move, current_question) for move in state.non_processed_moves):
                    return True

    @staticmethod
    def effects(state: DialogState):
        state.next_moves.insert(0, NegativeUnderstanding())
        state.non_processed_moves = []


class ExecTryRule(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.agenda) > 0 and isinstance(state.agenda[0], TryRule)

    @staticmethod
    def effects(state: DialogState):
        rule = state.agenda.pop(0).rule
        try_rule(state, rule)
