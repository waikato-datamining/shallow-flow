from .actor import Actor
from .config import ConfigItem
from .director import SequentialDirector


class ActorHandler(Actor):
    """
    Interface for actors that manage sub-actors.
    """

    def initialize(self):
        """
        Performs initializations.
        """
        super(ActorHandler, self).initialize()
        self._configmanager.add(ConfigItem("actors", list, list(), "The sub-actors to manage"))

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
        return self._configmanager.get("actors")

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
        self._configmanager.set("actors", actors)

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        return self._director().execute(self.actors)


class Flow(ActorHandler):
    """
    Encapsulates a complete flow.
    """

    def _director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(requires_source=True, requires_sink=False)
