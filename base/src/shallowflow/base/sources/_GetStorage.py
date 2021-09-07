from shallowflow.api.source import AbstractSimpleSource
from shallowflow.api.config import Option
from shallowflow.api.storage import is_valid_name
from shallowflow.api.compatibility import Unknown


class GetStorage(AbstractSimpleSource):
    """
    Outputs the value of the specified storage item.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Outputs the value of the specified storage item."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="storage_name", value_type=str, def_value="storage",
                                        help="The name of the storage item"))

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
        result = None
        name = self.get("storage_name")
        if self.storage_handler.storage.has(name):
            self._output.append(self.storage_handler.storage.get(name))
        else:
            result = "Storage item not available: %s" % name
        return result
