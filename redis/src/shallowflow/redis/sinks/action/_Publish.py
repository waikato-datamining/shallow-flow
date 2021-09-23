from ._AbstractAction import AbstractAction
from shallowflow.api.config import Option


class Publish(AbstractAction):
    """
    Publishes the incoming message to the specified channel.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Publishes the incoming message to the specified channel."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("as_string", bool, False, "If enabled, the data gets treated as string"))
        self._option_manager.add(Option("channel", str, "", "The channel to publish on."))

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [str]

    def _check(self, connection, o):
        """
        Performs checks before performing the action.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to use
        :rtype: str
        """
        result = super()._check(connection, o)
        if result is None:
            if len(self.get("channel")) == 0:
                result = "No channel supplied!"
        return result

    def _do_execute(self, connection, o):
        """
        Executes the action using the object and the specified connection.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to use
        :return: None if successful, otherwise error message
        :rtype: str
        """
        as_string = self.get("as_string")
        if as_string:
            o = str(o)
        channel = self.get("channel")
        if self.is_debug:
            self.log("%s -> %s" % (channel, o))
        connection.publish(channel, o)
        return None
