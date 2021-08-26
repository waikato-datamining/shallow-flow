import re
from shallowflow.api.source import AbstractListOutputSource
from shallowflow.api.config import Option


class ListStorage(AbstractListOutputSource):
    """
    Outputs the names of the current storage items.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Outputs the names of the current storage items."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="filter", value_type=str, def_value=",*",
                                        help="The regular expression that the names must match"))
        self._option_manager.add(Option(name="invert", value_type=bool, def_value=False,
                                        help="Whether to invert the matching sense"))

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if self.storage_handler is None:
                result = "No storage handler available!"
        return result

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None

        filter = self.get("filter")
        invert = self.get("invert")
        pattern = re.compile(filter)
        for k in self.storage_handler.storage.keys():
            match = pattern.fullmatch(k)
            if invert:
                match = not match
            if match:
                self._output.append(k)
        return result
