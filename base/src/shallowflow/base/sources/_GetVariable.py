from shallowflow.api.source import AbstractSimpleSource
from shallowflow.api.config import Option
from shallowflow.api.vars import VariableName
from shallowflow.api.compatibility import Unknown


class GetVariable(AbstractSimpleSource):
    """
    Outputs the value of the specified variable.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Outputs the value of the specified variable."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="var_name", value_type=VariableName, def_value=VariableName("var"),
                                        help="The name of the variable"))

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
        result = None
        name = self.get("var_name")
        if self.variables.has(name):
            self._output.append(self.variables.get(name))
        else:
            result = "Variable not available: %s" % name
        return result
