import re
from shallowflow.api.source import AbstractListOutputSource
from shallowflow.api.config import Option


class ListVariables(AbstractListOutputSource):
    """
    Outputs the names of the current variables.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Outputs the names of the current variables."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="filter", value_type=str, def_value=",*",
                                        help="The regular expression that the names must match"))
        self._option_manager.add(Option(name="invert", value_type=bool, def_value=False,
                                        help="Whether to invert the matching sense"))

    def _get_item_type(self):
        """
        Returns the type of the individual items that get generated, when not outputting a list.

        :return: the type that gets generated
        """
        return str

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
        for k in self.variables.keys():
            match = pattern.fullmatch(k)
            if invert:
                match = not match
            if match:
                self._output.append(k)
        return result
