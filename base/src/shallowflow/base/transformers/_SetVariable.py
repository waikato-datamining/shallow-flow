from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.config import Option
from shallowflow.api.vars import VariableName
from shallowflow.api.compatibility import Unknown
import shallowflow.api.serialization.vars as ser_vars


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
        self._option_manager.add(Option(name="var_name", value_type=VariableName, def_value=VariableName("var"),
                                        help="The name of the variable"))
        self._option_manager.add(Option(name="var_value", value_type=str, def_value="",
                                        help="The value to use instead of data passing through"))
        self._option_manager.add(Option(name="expand", value_type=bool, def_value=False,
                                        help="Whether to expand any variables in the value."))

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
            if len(self.get("var_name")) == 0:
                result = "No variable name provided!"
        return result

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        value = self.get("var_value")
        if self.get("expand"):
            value = self.variables.expand(value)
            if self.is_debug:
                self.log("'%s' expanded to '%s'" % (self.get("var_value"), value))
        name = self.get("var_name")
        if len(value) == 0:
            value = self._input
        if ser_vars.has_string_writer(type(value)):
            writer = ser_vars.get_string_writer(type(value))()
            value_str = writer.convert(value)
        else:
            self.log("Failed to determine string conversion for type: %s" % str(type(value)))
            value_str = str(value)
        if self.is_debug:
            self.log("%s -> %s" % (name, value_str))
        self.variables.set(name, value_str)
        self._output.append(self._input)
        return None
