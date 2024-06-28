from isupy.ontology import DialogState


def try_rule(state: DialogState, rule):
    result = rule.preconditions(state)
    if result:
        try:
            bound_variables = list(result)
        except TypeError:
            bound_variables = None
        if bound_variables:
            rule.effects(state, *bound_variables)
        else:
            rule.effects(state)
