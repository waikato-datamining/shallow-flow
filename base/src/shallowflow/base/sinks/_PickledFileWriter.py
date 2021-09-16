import pickle
from shallowflow.api.sink import AbstractFileWriter
from shallowflow.api.compatibility import Unknown


class PickledFileWriter(AbstractFileWriter):
    """
    Pickles the incoming object and writes it to the specified file.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Pickles the incoming object and writes it to the specified file."

    def accepts(self):
        """
        Returns the types that are accepted.

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
        fname = self.variables.expand(self.get("output_file"))
        try:
            with open(fname, "wb") as f:
                pickle.dump(self._input, f)
        except Exception:
            result = self._handle_exception("Failed to write object to: %s" % fname)
        return result
