import cv2
import numpy
from shallowflow.base.conversions import AbstractConversion


class FrameToJpgBytes(AbstractConversion):
    """
    Converts a CV2 frame to a JPG (bytes).
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Converts a CV2 frame to a JPG (bytes)."

    def accepts(self):
        """
        Returns the type that the conversion accepts.

        :return: the type
        """
        return numpy.ndarray

    def generates(self):
        """
        Returns the type that the conversion generates.

        :return: the type
        """
        return bytes

    def _do_convert(self, o):
        """
        Performs the conversion.

        :param o: the object to convert
        :return: the converted object
        """
        return cv2.imencode('.jpg', o)[1].tobytes()


class JpgBytesToFrame(AbstractConversion):
    """
    Converts JPG bytes to a CV2 frame.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Converts a CV2 frame to a JPG (bytes)."

    def accepts(self):
        """
        Returns the type that the conversion accepts.

        :return: the type
        """
        return bytes

    def generates(self):
        """
        Returns the type that the conversion generates.

        :return: the type
        """
        return numpy.ndarray

    def _do_convert(self, o):
        """
        Performs the conversion.

        :param o: the object to convert
        :return: the converted object
        """
        array = numpy.fromstring(o, numpy.uint8)
        return cv2.imdecode(array, cv2.IMREAD_COLOR)
