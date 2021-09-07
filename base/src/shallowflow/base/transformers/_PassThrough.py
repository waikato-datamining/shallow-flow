from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.compatibility import Unknown


class PassThrough(AbstractSimpleTransformer):
    """
    Dummy, just passes through the data.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Dummy, just passes through the data."

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [Unknown]

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [Unknown]

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._output.append(self._input)
        return None
