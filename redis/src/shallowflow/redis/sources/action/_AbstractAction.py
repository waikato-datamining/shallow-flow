import redis
from shallowflow.api.config import AbstractOptionHandler, optionhandler_to_dict, dict_to_optionhandler
from shallowflow.api.serialization.objects import add_dict_writer, add_dict_reader


class AbstractAction(AbstractOptionHandler):
    """
    Ancestor for Redis actions.
    """

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        raise NotImplemented()

    def _check(self, connection):
        """
        Performs checks before performing the action.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :rtype: str
        """
        if connection is None:
            return "No Redis connection!"
        return None

    def _do_execute(self, connection):
        """
        Executes the action using the specified connection and forwards the object.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :return: the retrieved object, None if not available
        """
        raise NotImplemented()

    def execute(self, connection):
        """
        Executes the action using the specified connection and forwards the object.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :return: the retrieved object, None if not available
        """
        msg = self._check(connection)
        if msg is not None:
            raise Exception(msg)
        return self._do_execute(connection)


# register reader/writer
add_dict_writer(AbstractAction, optionhandler_to_dict)
add_dict_reader(AbstractAction, dict_to_optionhandler)
