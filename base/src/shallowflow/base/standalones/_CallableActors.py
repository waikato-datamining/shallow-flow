from shallowflow.api.callable import ActorReferenceHandler
from shallowflow.api.director import AbstractDirector


class CallableActorsDirector(AbstractDirector):
    """
    The director for CallableActors.
    """

    def _do_execute(self, actors):
        """
        Executes the specified list of actors.

        :param actors: the actors to execute
        :type actors: list
        :return: None if successfully executed, otherwise error message
        :rtype: str
        """
        return None


class CallableActors(ActorReferenceHandler):
    """
    Manages actors that can be referenced by their name.
    """

    def _check_actors(self, actors):
        """
        Performs checks on the sub-actors.

        :param actors: the actors to check
        :type actors: list
        :return: None if successful check, otherwise error message
        :rtype: str
        """
        result = super()._check_actors(actors)

        if result is None:
            handler = self.scope_handler
            if handler is not None:
                for actor in actors:
                    msg = handler.add_callable_name(self, actor)
                    if msg is not None:
                        result = msg
                        break

        return result

    def _new_director(self):
        """
        Returns the director to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return CallableActorsDirector(self)
