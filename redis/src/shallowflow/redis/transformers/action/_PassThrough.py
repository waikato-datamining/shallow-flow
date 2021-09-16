from ._AbstractAction import AbstractAction
from shallowflow.api.compatibility import Unknown


class PassThrough(AbstractAction):
    """
    Just passes through the data, no redis interaction.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Just passes through the data, no redis interaction."

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [Unknown]

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [Unknown]

    def _do_execute(self, connection, o):
        """
        Executes the action using the specified connection and forwards the object.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to use
        :return: the retrieved object, None if not available
        """
        return o
