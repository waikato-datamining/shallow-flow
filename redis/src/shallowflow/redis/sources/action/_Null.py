from ._AbstractAction import AbstractAction
from shallowflow.api.compatibility import Unknown


class Null(AbstractAction):
    """
    Dummy, does not retrieve anything.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Dummy, does not retrieve anything."

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [Unknown]

    def _do_execute(self, connection):
        """
        Executes the action using the specified connection and forwards the object.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :return: the retrieved object, None if not available
        """
        return None
