from ._AbstractAction import AbstractAction


class Null(AbstractAction):
    """
    Dummy action, does nothing.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Dummy action, does nothing."

    def _do_execute(self, connection, o):
        """
        Executes the action using the object and the specified connection.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to use
        :return: None if successful, otherwise error message
        :rtype: str
        """
        return None
