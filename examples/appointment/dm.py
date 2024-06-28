from isupy.rule import Rule
from isupy.isu import try_rule
import isupy.dm

from examples.appointment.ontology import *


class DialogueManager(isupy.dm.DialogueManager):
    def get_system_move(self, state):
        try_rule(state, GetLatestMoves)
        return state.next_system_move

    def set_user_move(self, state, move):
        state.user_move = move


class GetLatestMoves(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return True

    @staticmethod
    def effects(state: DialogState):
        if state.user_input and state.user_input.move:
            state.private.non_integrated_moves.append(state.user_input.move)
            state.shared.latest_moves.append(state.user_input.move)
