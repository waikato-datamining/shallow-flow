from shallowflow.api.actor import OutputProducer
from shallowflow.api.callable import AbstractCallableActor
from shallowflow.api.compatibility import Unknown


class CallableSource(AbstractCallableActor, OutputProducer):
    """
    Executes the referenced source.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Executes the referenced source."

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
        return self._callable_actor.execute()

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
