from shallowflow.api.control import MutableActorHandler
from shallowflow.base.directors import SequentialDirector


class Sequence(MutableActorHandler):
    """
    Executes the sub-actors one after the other, with the output of an actor being the input for the next; the first actor must accept input.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Executes the sub-actors one after the other, with the output of an actor being the input for the next; the first actor must accept input."

    def _new_director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, allows_standalones=False, requires_source=True, requires_sink=False)
