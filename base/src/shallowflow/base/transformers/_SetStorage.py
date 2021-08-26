from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.config import Option
from shallowflow.api.vars import is_valid_name
import shallowflow.api.serialization.vars as ser_vars


class SetStorage(AbstractSimpleTransformer):
    """
    Stores the value coming through in storage under the specified name.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Stores the value coming through in storage under the specified name."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="storage_name", value_type=str, def_value="storage",
                                        help="The name of the storage item"))

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if self.storage_handler is None:
                result = "No storage handler available!"
        if result is None:
            if len(self.get("storage_name")) == 0:
                result = "No storage name provided!"
            elif not is_valid_name(self.get("storage_name")):
                result = "Not a valid storage name: %s" + self.get("storage_name")
        return result

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        name = self.get("storage_name")
        value = self._input
        self.storage_handler.storage.set(name, value)
        self._output.append(self._input)
        return None
