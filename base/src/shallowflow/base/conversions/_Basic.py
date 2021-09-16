from shallowflow.api.compatibility import Unknown
from ._AbstractConversion import AbstractConversion


class PassThrough(AbstractConversion):
    """
    Just passes through the object.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Just passes through the object."

    def accepts(self):
        """
        Returns the type that the conversion accepts.

        :return: the type
        """
        return Unknown

    def generates(self):
        """
        Returns the type that the conversion generates.

        :return: the type
        """
        return Unknown

    def _do_convert(self, o):
        """
        Performs the conversion.

        :param o: the object to convert
        :return: the converted object
        """
        return o
