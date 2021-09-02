from shallowflow.api.config import Option
from shallowflow.api.help import AbstractHelpGenerator


class Markdown(AbstractHelpGenerator):
    """
    Generates help in plain text format.
    """

    def file_extension(self):
        """
        Returns the preferred file extension.

        :return: the file extension (incl dot)
        :rtype: str
        """
        return ".md"

    def _indent(self, s, num):
        """
        Indents the lines in the string.

        :param s: the string to indent
        :type s: str
        :param num: the number of spaces to use for indentation
        :type num: int
        :return: the indented string
        :rtype: str
        """
        if num == 0:
            return s
        indent = " " * num
        parts = s.split("\n")
        result = ""
        for part in parts:
            if len(result) > 0:
                result += "\n"
            result += indent + part
        return result

    def _do_generate(self, handler):
        """
        Performs the actual generation.

        :param handler: the option handler to generate the help for
        :type handler: AbstractOptionHandler
        :return: the generate string
        :rtype: str
        """
        result = "# " + type(handler).__name__ + "\n"
        result += "\n"

        result += "## Description\n"
        result += handler.description() + "\n"
        result += "\n"

        result += "## Options\n"
        for item in handler.option_manager.options():
            result += "* " + item.name + " (" + str(item.value_type.__name__) + ")\n"
            result += "\n"
            result += "  * " + item.help + "\n"
            result += "  * default: " + repr(item.def_value) + "\n"
            result += "\n"

        return result
