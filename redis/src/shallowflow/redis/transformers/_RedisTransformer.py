from shallowflow.api.actor_utils import find_closest_type
from shallowflow.api.class_utils import get_class_name
from shallowflow.api.config import Option
from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.redis.transformers.action import AbstractAction, PassThrough
from shallowflow.redis.standalones import RedisConnection


class RedisTransformer(AbstractSimpleTransformer):
    """
    Applies the specified Redis action to the incoming data and forwards the generated data.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Applies the specified Redis action to the incoming data and forwards the generated data."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("action", AbstractAction, PassThrough(), "The Redis action to perform"))

    def reset(self):
        """
        Resets the state of the actor.
        """
        super().reset()
        self._connection = None

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return self.get("action").accepts()

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return self.get("action").generates()

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            self._connection = find_closest_type(self, RedisConnection, include_same_level=True)
            if self._connection is None:
                result = "Failed to locate %s!" % get_class_name(RedisConnection)

        return result

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        action = self.get("action")
        try:
            output = action.execute(self._connection.connection, self._input)
            if output is not None:
                self._output.append(output)
        except Exception:
            result = self._handle_exception("Failed to execute action %s!" % get_class_name(action))
        return result

    def stop_execution(self):
        """
        Stops the actor execution.
        """
        self.get("action").stop_execution()
        super().stop_execution()
