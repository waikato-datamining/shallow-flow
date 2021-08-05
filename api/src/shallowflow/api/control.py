from .actor import Actor, actor_to_dict, dict_to_actor
from .config import Option


class ActorHandler(Actor):
    """
    Interface for actors that manage sub-actors.
    """

    def initialize(self):
        """
        Performs initializations.
        """
        super(ActorHandler, self).initialize()
        self.option_manager.add(Option("actors", list, list(), "The sub-actors to manage", Actor))
        self.option_manager.set_to_dict_handler("actors", actor_list_to_dict_list)
        self.option_manager.set_from_dict_handler("actors", dict_list_to_actor_list)

    def _director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        raise NotImplemented()

    @property
    def actors(self):
        """
        Returns the current sub-actors.

        :return: the sub-actors
        :rtype: list
        """
        return self._option_manager.get("actors")

    @actors.setter
    def actors(self, actors):
        """
        Sets the new sub-actors.

        :param actors: the new actors
        :type actors: list
        """
        for a in actors:
            if not isinstance(a, Actor):
                raise Exception("Can only set objects of type Actor!")
            a.parent = self
        self._option_manager.set("actors", actors)

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        return self._director().execute(self.actors)


def dict_list_to_actor_list(l):
    result = []
    for d in l:
        result.append(dict_to_actor(d))
    return result


def actor_list_to_dict_list(l):
    result = []
    for actor in l:
        result.append(actor_to_dict(actor))
    return result
