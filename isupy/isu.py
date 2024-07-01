from isupy.ontology import DialogState
from isupy.logger import logger


def try_rule(state: DialogState, rule):
    logger.debug('try_rule', rule=rule)
    result = rule.preconditions(state)
    if result:
        logger.info('preconditions true')
        try:
            bound_variables = list(result)
        except TypeError:
            bound_variables = None
        if bound_variables:
            rule.effects(state, *bound_variables)
        else:
            rule.effects(state)
