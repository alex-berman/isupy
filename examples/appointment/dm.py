from isupy.rule import Rule
from isupy.isu import try_rule
import isupy.dm

from examples.appointment.ontology import *


class DialogueManager(isupy.dm.DialogueManager):
    def get_next_moves(self, state):
        try_rule(state, SelectGreet)
        return state.next_moves

    def set_latest_move(self, state, move):
        state.user_move = move


class SelectGreet(Rule):
    @staticmethod
    def preconditions(state: DialogState):
        return len(state.private.agenda) > 0 and state.private.agenda[0] == GreetAction()

    @staticmethod
    def effects(state: DialogState):
        state.next_moves.append(Greet())
