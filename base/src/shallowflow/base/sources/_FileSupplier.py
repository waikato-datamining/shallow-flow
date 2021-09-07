from shallowflow.api.source import AbstractListOutputSource
from shallowflow.api.config import Option
from shallowflow.api.io import File


class FileSupplier(AbstractListOutputSource):
    """
    Outputs the specified files.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Outputs the specified files."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="files", value_type=list, def_value=list(),
                                        help="The files to output", base_type=File))

    def _get_item_type(self):
        """
        Returns the type of the individual items that get generated, when not outputting a list.

        :return: the type that gets generated
        """
        return File

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._output.extend(self.get("files"))
        return None
