from .actor import Actor
from .control import ActorHandler


def find_actor_handlers(actor, must_allow_standalones=False, include_same_level=False):
    """
    Returns a list of actor handlers, starting from the current node (excluded).
    The search goes up in the actor hierarchy, up to the root (i.e., the last
    item in the returned list will be most likely a "Flow" actor).

    :param actor: the starting point
    :type actor: Actor
    :param must_allow_standalones: whether the handler must allow standalones
    :type must_allow_standalones: bool
    :param include_same_level: allows adding of actor handlers that are on
                               the same level as the current actor, but
                               are before it
    :return: the handlers
    :rtype: list
    """
    result = []
    root = actor.root
    child = actor
    parent = actor.parent
    while parent is not None:
        if isinstance(parent, ActorHandler):
            handler = parent
            if include_same_level:
                index = handler.index(child.name)
                for i in range(index - 1, -1, -1):
                    sub_handler = None
                    # TODO external flows
                    if isinstance(handler.actors[i], ActorHandler):
                        sub_handler = handler.actors[i]
                    if sub_handler is None:
                        continue
                    if must_allow_standalones:
                        if sub_handler.actor_handler_info.can_contain_standalones:
                            result.append(sub_handler)
                    else:
                        result.append(sub_handler)
            else:
                if must_allow_standalones:
                    if handler.actor_handler_info.can_contain_standalones:
                        result.append(handler)
                else:
                    result.append(handler)

        if parent == root:
            parent = None
        else:
            child = parent
            parent = parent.parent

    return result
