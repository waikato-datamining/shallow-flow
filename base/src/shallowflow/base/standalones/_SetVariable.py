import os
from shallowflow.api.actor import Actor
from shallowflow.api.config import Option
from shallowflow.api.vars import VariableName


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
        self._option_manager.add(Option(name="var_name", value_type=VariableName, def_value=VariableName("var"),
                                        help="The name of the variable"))
        self._option_manager.add(Option(name="var_value", value_type=str, def_value="",
                                        help="The value to use instead of data passing through"))
        self._option_manager.add(Option(name="env_var", value_type=str, def_value="",
                                        help="The environment variable to use for setting the value (overrides 'var_value')."))
        self._option_manager.add(Option(name="env_var_optional", value_type=bool, def_value=False,
                                        help="Whether the environment must exist or can be absent."))
        self._option_manager.add(Option(name="expand", value_type=bool, def_value=False,
                                        help="Whether to expand any variables in the value."))

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
        result = None

        value = self.get("var_value")
        env_var = self.get("env_var")
        if len(env_var) > 0:
            if os.getenv(env_var) is None:
                if not self.get("env_var_optional"):
                    result = "Environment variable not present: %s" % env_var
            else:
                value = os.getenv(env_var)

        if result is None:
            if self.get("expand"):
                value = self.variables.expand(value)
                if self.is_debug:
                    self.log("'%s' expanded to '%s'" % (self.get("var_value"), value))
            name = self.get("var_name")
            self.variables.set(name, value)

        return result
