import os
import re
from shallowflow.api.source import AbstractSimpleSource
from shallowflow.api.config import Option


class DirectoryLister(AbstractSimpleSource):
    """
    Lists files or dirs in a directory.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Lists dirs and/or files in the specified directory."

    def initialize(self):
        """
        Performs initializations.
        """
        super(DirectoryLister, self).initialize()
        self._option_manager.add(Option("dir", str, ".", "The directory to use for listing files/dirs"))
        self._option_manager.add(Option("list_files", bool, False, "If enabled, files get listed"))
        self._option_manager.add(Option("list_dirs", bool, False, "If enabled, dirs get listed"))
        self._option_manager.add(Option("max_items", int, -1, "The maximum number of files/dirs to list, ignored if <=0"))
        self._option_manager.add(Option("regexp", str, "", "The regular expression that the files/dirs must match, ignored if empty string"))
        self._option_manager.add(Option("recursive", bool, False, "If enabled, looking for files/dirs recursively"))
        self._option_manager.add(Option("sort", bool, False, "If enabled, the located files/dirs get sorted"))

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if sucessful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if not os.path.exists(self._option_manager.get("dir")):
                result = "Directory does not exist: %s" % self._option_manager.get("dir")
            elif not os.path.isdir(self._option_manager.get("dir")):
                result = "Does not point to a directory: %s" % self._option_manager.get("dir")
        return result

    def _search(self, dir):
        """
        Searches the specified directory.

        :param dir: the directory to search
        :type dir: str
        """
        for f in os.listdir(dir):
            full = os.path.join(dir, f)
            if (self.get("max_items") > 0) and (len(self._output) >= self.get("max_items")):
                break
            if len(self.get("regexp")) > 0:
                if not re.search(self.get("regexp"), f):
                    continue
            if self.get("list_files") and os.path.isfile(full):
                self._output.append(full)
            elif self.get("list_dirs") and os.path.isdir(full):
                self._output.append(full)
            if os.path.isdir(full) and self.get("recursive"):
                self._search(full)

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._search(self.get("dir"))
        return None
