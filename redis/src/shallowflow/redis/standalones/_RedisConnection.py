import redis
from shallowflow.api.actor import Actor
from shallowflow.api.config import Option

STATE_CONNECTION = "connection"


class RedisConnection(Actor):
    """
    Manages the connection to the Redis server.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Manages the connection to the Redis server."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="host", value_type=str, def_value="localhost",
                                        help="The Redis host to connect to"))
        self._option_manager.add(Option(name="port", value_type=int, def_value=6379,
                                        help="The port the Redis instance is listening on"))
        self._option_manager.add(Option(name="db", value_type=int, def_value=0,
                                        help="The database to use."))

    def reset(self):
        """
        Resets the state of the object.
        """
        super().reset()
        self._connection = None

    def _backup_state(self):
        """
        For backing up the internal state before reconfiguring due to variable changes.

        :return: the state dictionary
        :rtype: dict
        """
        result = super()._backup_state()
        if self._connection is not None:
            result[STATE_CONNECTION] = self._connection
        return result

    def _restore_state(self, state):
        """
        Restores the state from the state dictionary after being reconfigured due to variable changes.

        :param state: the state dictionary to use
        :type state: dict
        """
        if STATE_CONNECTION in state:
            self._connection = state[STATE_CONNECTION]
            del state[STATE_CONNECTION]
        super()._restore_state(state)

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        host = self.get("host")
        port = self.get("port")
        db = self.get("db")
        try:
            self._connection = redis.Redis(host=host, port=port, db=db)
        except Exception:
            result = self._handle_exception("Failed to connect to Redis host: %s/%d/%d" % (host, port, db))

        return result

    @property
    def connection(self):
        """
        Returns the current Redis connection.

        :return: the connection, None if none available
        :rtype: redis.Redis
        """
        return self._connection

    def wrap_up(self):
        """
        For finishing up the execution.
        Does not affect graphical output.
        """
        if self._connection is not None:
            self._connection.close()
            self._connection = None
        super().wrap_up()
