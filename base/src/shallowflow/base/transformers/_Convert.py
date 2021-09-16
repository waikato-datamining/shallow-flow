from shallowflow.api.config import Option
from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.base.conversions import AbstractConversion, PassThrough


class Convert(AbstractSimpleTransformer):
    """
    Applies the specified conversion to the data passing through.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Applies the specified conversion to the data passing through."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="conversion", value_type=AbstractConversion, def_value=PassThrough(),
                                        help="The conversion to apply to the data"))

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [self.get("conversion").accepts()]

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [self.get("conversion").generates()]

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        conversion = self.get("conversion")
        try:
            conversion.flow_context = self
            self._output.append(conversion.convert(self._input))
        except Exception:
            result = self._handle_exception("Failed to convert input data!")
        return result
