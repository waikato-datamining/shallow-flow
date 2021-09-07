from time import sleep
from shallowflow.api.config import Option
from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.compatibility import Unknown


class Sleep(AbstractSimpleTransformer):
    """
    Pauses execution for the specified number of seconds.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Pauses execution for the specified number of seconds."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="seconds", value_type=float, def_value=1.0, lower=0.0,
                                        help="The number of seconds to wait"))

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
        seconds = self.get("seconds")
        if seconds > 0:
            sleep(seconds)
        self._output.append(self._input)
        return None
