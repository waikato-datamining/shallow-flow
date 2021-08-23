from .config import AbstractOptionHandler


class AbstractHelpGenerator(AbstractOptionHandler):
    """
    Ancestor for classes that generate help from option handlers.
    """

    def _do_generate(self, handler):
        """
        Performs the actual generation.

        :param handler: the option handler to generate the help for
        :type handler: AbstractOptionHandler
        :return: the generate string
        :rtype: str
        """
        raise NotImplemented()

    def generate(self, handler, fname=None):
        """
        Generates help for the supplied option handler.

        :param handler: the option handler to generate the help for
        :type handler: AbstractOptionHandler
        :param fname: the file to store the help in, uses stdout if not provided
        :type fname: str
        """

        help = self._do_generate(handler)
        if fname is None:
            print(help)
        else:
            with open(fname, "w") as hf:
                hf.write(help)
