import redis
from shallowflow.api.config import AbstractOptionHandler, optionhandler_to_dict, dict_to_optionhandler
from shallowflow.api.serialization.objects import add_dict_writer, add_dict_reader


class AbstractAction(AbstractOptionHandler):
    """
    Ancestor for Redis actions.
    """

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        raise NotImplemented()

    def _check(self, connection, o):
        """
        Performs checks before performing the action.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to use
        :rtype: str
        """
        if connection is None:
            return "No Redis connection!"
        if o is None:
            return "No object provided for action!"
        return None

    def _do_execute(self, connection, o):
        """
        Executes the action using the object and the specified connection.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to use
        :return: None if successful, otherwise error message
        :rtype: str
        """
        raise NotImplemented()

    def execute(self, connection, o):
        """
        Executes the action using the object and the specified connection.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to send
        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = self._check(connection, o)
        if result is None:
            result = self._do_execute(connection, o)
        return result


# register reader/writer
add_dict_writer(AbstractAction, optionhandler_to_dict)
add_dict_reader(AbstractAction, dict_to_optionhandler)
