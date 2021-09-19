from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.config import Option
from shallowflow.api.vars import VariableName
from shallowflow.api.compatibility import Unknown


class IncVariable(AbstractSimpleTransformer):
    """
    Increments the value of variable by the specified value.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Increments the value of variable by the specified value."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="var_name", value_type=VariableName, def_value=VariableName("var"),
                                        help="The name of the variable to increment"))
        self._option_manager.add(Option(name="inc_value", value_type=str, def_value="1",
                                        help="The value to increment the variable by"))
        self._option_manager.add(Option(name="is_float", value_type=bool, def_value=False,
                                        help="Whether to increment an integer or float variable"))

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

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            name = self.get("var_name")
            value = self.get("inc_value")
            if len(name) == 0:
                result = "No variable name provided!"
            elif len(value) == 0:
                result = "No increment value provided!"
            elif not self.get("is_float"):
                try:
                    int(value)
                except Exception:
                    result = "Increment value is not an integer: %s" % value
            elif self.get("is_float"):
                try:
                    float(value)
                except Exception:
                    result = "Increment value is not a float: %s" % value
        return result

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        inc = self.get("inc_value")
        name = self.get("var_name")
        is_float = self.get("is_float")
        if self.variables.has(name):
            value = self.variables.get(name)
        else:
            value = "0"
        if is_float:
            value_new = float(value) + float(inc)
        else:
            value_new = int(value) + int(inc)
        value_new = str(value_new)
        self.variables.set(name, value_new)
        if self.is_debug:
            self.log("Incremented variable: %s -> %s" % (value, value_new))
        self._output.append(self._input)
        return None
