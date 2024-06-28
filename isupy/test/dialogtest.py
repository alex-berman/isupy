import pytest

from isupy.semantic_serialization import deserialize


def parse_turn_content(turn_content):
    speaker = turn_content[0]
    contribution = turn_content[2:]
    return speaker, contribution


def run_dialog_test_sem(dm, turns, state):
    for turn_content in turns:
        speaker, move_representation = parse_turn_content(turn_content)
        handle_turn_sem(dm, speaker, move_representation, state)


def handle_turn_sem(dm, speaker, move_representation, state):
    if speaker == 'S':
        expected_system_move = None if move_representation == '' else deserialize(move_representation)
        try:
            actual_system_move = dm.get_system_move(state)
        except:
            pytest.fail(f'Exception raised when expecting system move {move_representation}')
            raise
        assert actual_system_move == expected_system_move
    elif speaker == 'U':
        move = deserialize(move_representation)
        state.user_input = UserInput(move=move)
