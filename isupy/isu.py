from isupy.ontology import DialogState
from isupy.logger import logger


def try_rule(state: DialogState, rule):
    logger.debug('try_rule', rule=rule, state=state)
    result = rule.preconditions(state)
    if result:
        logger.info('preconditions true')
        if isinstance(result, dict):
            rule.effects(state, **result)
        else:
            rule.effects(state)
