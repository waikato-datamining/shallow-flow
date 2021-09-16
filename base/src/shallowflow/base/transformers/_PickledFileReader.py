import pickle
from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.compatibility import Unknown
from shallowflow.api.io import File


class PickledFileReader(AbstractSimpleTransformer):
    """
    Unpickles the object from the incoming file and forwards it.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Unpickles the object from the incoming file and forwards it."

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [File]

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
        result = None
        try:
            with open(self._input, "rb") as f:
                self._output.append(pickle.load(f))
        except Exception:
            result = self._handle_exception("Failed to read object from: %s" % self._input)
        return result
