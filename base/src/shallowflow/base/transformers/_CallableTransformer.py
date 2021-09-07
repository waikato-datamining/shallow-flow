from shallowflow.api.actor import InputConsumer, OutputProducer
from shallowflow.api.callable import AbstractCallableActor
from shallowflow.api.compatibility import Unknown

STATE_INPUT = "input"


class CallableTransformer(AbstractCallableActor, InputConsumer, OutputProducer):
    """
    Executes the referenced transformer.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Executes the referenced transformer."

    def reset(self):
        """
        Resets the state of the actor.
        """
        super().reset()
        self._input = None

    def input(self, data):
        """
        Sets the input data to consume.

        :param data: the data to consume
        :type data: object
        """
        self._input = data

    def _backup_state(self):
        """
        For backing up the internal state before reconfiguring due to variable changes.

        :return: the state dictionary
        :rtype: dict
        """
        result = super()._backup_state()
        if self._input is not None:
            result[STATE_INPUT] = self._input
        return result

    def _restore_state(self, state):
        """
        Restores the state from the state dictionary after being reconfigured due to variable changes.

        :param state: the state dictionary to use
        :type state: dict
        """
        if STATE_INPUT in state:
            self._input = state[STATE_INPUT]
            del state[STATE_INPUT]
        super()._restore_state(state)

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        if self._callable_actor is not None:
            return self._callable_actor.accepts()
        else:
            return [Unknown]

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        if self._callable_actor is not None:
            return self._callable_actor.generates()
        else:
            return [Unknown]

    def _do_execute_callable_actor(self):
        """
        Executes the callable actor.

        :return: None if successfully executed, otherwise error message
        :rtype: str
        """
        if self._input is not None:
            self._callable_actor.input(self._input)
        return self._callable_actor.execute()

    def _post_execute(self):
        """
        After the actual code got executed.
        """
        self._input = None
        super()._post_execute()

    def has_output(self):
        """
        Returns whether output data is available.

        :return: true if available
        :rtype: bool
        """
        return (self._callable_actor is not None) and self._callable_actor.has_output()

    def output(self):
        """
        Returns the next output data.

        :return: the data, None if nothing available
        :rtype: object
        """
        result = None
        if self._callable_actor is not None:
            result = self._callable_actor.output()
        return result

    def wrap_up(self):
        """
        For finishing up the execution.
        Does not affect graphical output.
        """
        self._input = None
        super().wrap_up()
