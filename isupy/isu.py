from typing import Callable, Any
from types import GeneratorType

from isupy.ontology import DialogState
from isupy.logger import logger


Rule = Callable[[DialogState], Any]


def try_rule(state: DialogState, rule: Rule):
    logger.debug('try_rule', rule=rule, state=state)
    result = rule(state)
    if result:
        if isinstance(result, GeneratorType):
            def get_first_item():
                for item in result:
                    return item

            conditional = get_first_item()
            if conditional:
                logger.info('preconditions true')

                def apply_effects():
                    try:
                        next(result)
                    except StopIteration:
                        pass

                apply_effects()
                return True


def repeat_until_none_applicable(state: DialogState, rules: list[Rule], max_iterations=100):
    num_iterations = 0
    while num_iterations < max_iterations:
        some_applicable = False
        for rule in rules:
            if try_rule(state, rule):
                some_applicable = True
        if not some_applicable:
            return
        num_iterations += 1
    raise Exception('Too many iterations')
