import cv2

from shallowflow.api.transformer import AbstractSimpleTransformer


class ImageFileReader(AbstractSimpleTransformer):
    """
    Loads the image.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Loads the image."

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        try:
            self._output.append(cv2.imread(self._input))
        except Exception:
            result = self._handle_exception("Failed to open image file: %s" % str(self._input))
        return result
