from shallowflow.api.control import ActorHandler
from shallowflow.api.storage import StorageHandler, Storage
from shallowflow.base.directors import SequentialDirector


class Flow(ActorHandler, StorageHandler):
    """
    Encapsulates a complete flow.
    """

    def _initialize(self):
        """
        Initializes the members.
        """
        super()._initialize()
        self._storage = Storage()

    def _new_director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, requires_source=True, requires_sink=False)

    @property
    def storage(self):
        """
        Returns the storage.

        :return: the storage
        :rtype: Storage
        """
        return self._storage


def run_flow(flow):
    """
    Executes the supplied flow.

    :param flow: the actor to execute
    :type flow: Actor
    :return: None if successful, otherwise error message
    :rtype: str
    """
    msg = flow.setup()
    if msg is None:
        msg = flow.execute()
        if msg is not None:
            return "Failed to execute flow: %s" % msg
    else:
        return "Failed to setup flow: %s" % msg
    flow.wrap_up()
    flow.clean_up()
