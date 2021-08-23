from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.config import Option
from shallowflow.api.vars import is_valid_name


class SetVariable(AbstractSimpleTransformer):
    """
    Stores the value coming through as variable under the specified name.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Stores the value coming through as variable under the specified name."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="var_name", value_type=str, def_value="var",
                                        help="The name of the variable"))
        self._option_manager.add(Option(name="var_value", value_type=str, def_value="",
                                        help="The value to use instead of data passing through"))

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if len(self.get("var_name")) == 0:
                result = "No variable name provided!"
            elif not is_valid_name(self.get("var_name")):
                result = "Not a valid variable name: %s" + self.get("var_name")
        return result

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        value = self.get("var_value")
        name = self.get("var_name")
        if len(value) == 0:
            self.variables.set(name, self._input)
        else:
            self.variables.set(name, value)
        self._output.append(self._input)
        return None
