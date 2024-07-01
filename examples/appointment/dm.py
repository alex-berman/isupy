from isupy.rule import Rule
from isupy.isu import try_rule
import isupy.dm
from isupy.logger import logger

from examples.appointment.ontology import *


class DialogueManager(isupy.dm.DialogueManager):
    @staticmethod
    def get_next_moves(state: DialogState):
        logger.debug('get_next_moves')
        state.next_moves = []
        try_rule(state, IntegrateRequest)
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
        return len(state.private.agenda) > 0 and state.private.agenda[0] == GreetAction()

    @staticmethod
    def effects(state: DialogState):
        state.private.agenda.pop(0)
        state.next_moves.append(Greet())


class SelectAsk(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.private.agenda) > 0 and isinstance(state.private.agenda[0], Findout)

    @staticmethod
    def effects(state: DialogState):
        state.next_moves.append(Ask(state.private.agenda[0].predicate))
        state.private.agenda.pop(0)


class IntegrateRequest(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.latest_moves) > 0 and state.latest_moves[0] == Request(CreateAppointment())

    @staticmethod
    def effects(state: DialogState):
        state.private.agenda = [
            Findout(WhQuestion(MeetingPerson)),
            Findout(WhQuestion(MeetingDate))
            ] + state.private.agenda
