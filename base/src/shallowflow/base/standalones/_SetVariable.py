from shallowflow.api.actor import Actor
from shallowflow.api.config import Option
from shallowflow.api.vars import is_valid_name
import shallowflow.api.serialization.vars as ser_vars


class SetVariable(Actor):
    """
    Stores the specified value under the specified name.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Stores the specified value under the specified name."

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
        if ser_vars.has_string_writer(type(value)):
            value_str = ser_vars.get_string_writer(type(value))().convert(value)
        else:
            self.log("Failed to determine string conversion for type: %s" % str(type(value)))
            value_str = str(value)
        self.variables.set(name, value_str)
        return None
