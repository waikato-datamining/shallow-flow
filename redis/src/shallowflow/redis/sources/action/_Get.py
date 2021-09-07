from ._AbstractAction import AbstractAction
from shallowflow.api.config import Option


class Get(AbstractAction):
    """
    Retrieves an object from the specified key.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Retrieves an object from the specified key."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("key", str, "", "The key to get the object from."))

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [str]

    def _check(self, connection):
        """
        Performs checks before performing the action.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :rtype: str
        """
        result = super()._check(connection)
        if result is None:
            if len(self.get("key")) == 0:
                result = "No key supplied!"
        return result

    def _do_execute(self, connection):
        """
        Executes the action using the specified connection and forwards the object.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :return: the retrieved object, None if not available
        """
        key = self.get("key")
        result = connection.get(key)
        if self.is_debug:
            self.log("%s -> %s" % (key, result))
        return result
