from isupy.ontology import DialogState
from isupy.logger import logger
from isupy.rule import Rule


def try_rule(state: DialogState, rule: Rule):
    logger.debug('try_rule', rule=rule, state=state)
    result = rule.preconditions(state)
    if result:
        logger.info('preconditions true')
        if isinstance(result, dict):
            rule.effects(state, **result)
        else:
            rule.effects(state)
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
