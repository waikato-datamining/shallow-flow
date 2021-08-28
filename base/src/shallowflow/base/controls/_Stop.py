from time import sleep
from shallowflow.api.config import Option
from shallowflow.api.transformer import AbstractSimpleTransformer


class Stop(AbstractSimpleTransformer):
    """
    Stops the flow.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Stops the flow."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="message", value_type=str, def_value="",
                                        help="The optional message to output; variables get expanded"))

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        msg = self.variables.expand(self.get("message"))
        if len(msg) > 0:
            self.log(msg)
        if self.root is not None:
            self.root.stop_execution()
        return None
