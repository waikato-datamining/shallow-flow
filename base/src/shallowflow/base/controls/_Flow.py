from shallowflow.api.control import ActorHandler
from shallowflow.api.director import SequentialDirector


class Flow(ActorHandler):
    """
    Encapsulates a complete flow.
    """

    def _new_director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, requires_source=True, requires_sink=False)
