import cv2
from shallowflow.api.sink import AbstractFileWriter


class ImageFileWriter(AbstractFileWriter):
    """
    Writes the incoming image data to disk.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Writes the incoming image data to disk."

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        fname = self.variables.expand(self.get("output_file"))
        try:
            cv2.imwrite(fname, self._input)
        except Exception:
            result = self._handle_exception("Failed to write image to %s" % fname)
        return result
