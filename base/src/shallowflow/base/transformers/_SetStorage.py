from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.config import Option
from shallowflow.api.storage import StorageUser, StorageName
from shallowflow.api.compatibility import Unknown


class SetStorage(AbstractSimpleTransformer, StorageUser):
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
        self._option_manager.add(Option(name="storage_name", value_type=StorageName, def_value=StorageName("storage"),
                                        help="The name of the storage item"))

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

    @property
    def uses_storage(self):
        """
        Returns whether storage is used.

        :return: True if used
        :rtype: bool
        """
        return not self.is_skipped

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
