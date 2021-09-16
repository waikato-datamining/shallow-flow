import redis
from shallowflow.api.config import AbstractOptionHandler, optionhandler_to_dict, dict_to_optionhandler
from shallowflow.api.stopping import Stoppable
from shallowflow.api.serialization.objects import add_dict_writer, add_dict_reader


class AbstractAction(AbstractOptionHandler, Stoppable):
    """
    Ancestor for Redis actions.
    """

    def _initialize(self):
        """
        Performs initializations.
        """
        super()._initialize()
        self._stopped = False

    def stop_execution(self):
        """
        Stops the actor execution.
        """
        self._stopped = True
        if self.is_debug:
            self.log("Stopped!")

    @property
    def is_stopped(self):
        """
        Returns whether the actor was stopped.

        :return: true if stopped
        :rtype: bool
        """
        return self._stopped

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        raise NotImplemented()

    def generates(self):
        """
        Returns the types that get generated.

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
        Executes the action using the specified connection and forwards the object.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to use
        :return: the retrieved object, None if not available
        """
        raise NotImplemented()

    def execute(self, connection, o):
        """
        Executes the action using the specified connection and forwards the object.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to use
        :return: the retrieved object, None if not available
        """
        self._stopped = False
        msg = self._check(connection, o)
        if msg is not None:
            raise Exception(msg)
        result = self._do_execute(connection, o)
        if self.is_stopped:
            return None
        else:
            return result


# register reader/writer
add_dict_writer(AbstractAction, optionhandler_to_dict)
add_dict_reader(AbstractAction, dict_to_optionhandler)
