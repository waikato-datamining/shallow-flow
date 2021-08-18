from shallowflow.api.sink import AbstractSimpleSink
from shallowflow.api.config import Option


class ConsoleOutput(AbstractSimpleSink):
    """
    Simply outputs the string representation of the incoming data to stdout.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Simply outputs the string representation of the incoming data to stdout."

    def initialize(self):
        """
        Performs initializations.
        """
        super().initialize()
        self._option_manager.add(Option(name="prefix", value_type=str, def_value="",
                                        help="The prefix to prepend to the output"))

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        print(self.get("prefix") + str(self._input))
        return None
