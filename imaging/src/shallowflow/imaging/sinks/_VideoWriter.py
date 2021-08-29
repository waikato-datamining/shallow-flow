import cv2
from shallowflow.api.config import Option
from shallowflow.api.sink import AbstractFileWriter

STATE_VIDEO_OUT = "video out"


class VideoWriter(AbstractFileWriter):
    """
    Writes the incoming image data to disk as MJPEG video.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Writes the incoming image data to disk as MJPEG video."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("fps", float, 30.0, "The frames-per-second to use in the output video."))

    def _output_file_help(self):
        """
        Returns the help string for the 'output_file' option.

        :return: the help string
        :rtype: str
        """
        return super()._output_file_help() + "; use .avi or .mkv as extension."

    def reset(self):
        """
        Resets the state of the actor.
        """
        super().reset()
        self._video_out = None

    def _backup_state(self):
        """
        For backing up the internal state before reconfiguring due to variable changes.

        :return: the state dictionary
        :rtype: dict
        """
        result = super()._backup_state()
        if self._video_out is not None:
            result[STATE_VIDEO_OUT] = self._video_out
        return result

    def _restore_state(self, state):
        """
        Restores the state from the state dictionary after being reconfigured due to variable changes.

        :param state: the state dictionary to use
        :type state: dict
        """
        if STATE_VIDEO_OUT in state:
            self._video_out = state[STATE_VIDEO_OUT]
            del state[STATE_VIDEO_OUT]
        super()._restore_state(state)

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        fname = self.variables.expand(self.get("output_file"))

        if self._video_out is None:
            try:
                frame_height, frame_width, _ = self._input.shape
                self._video_out = cv2.VideoWriter(fname, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.get("fps"),
                                                  (frame_width, frame_height))
            except Exception:
                result = self._handle_exception("Failed to open video output file: %s" % fname)

        try:
            self._video_out.write(self._input)
        except Exception:
            result = self._handle_exception("Failed to write image to %s" % fname)
        return result

    def wrap_up(self):
        """
        For finishing up the execution.
        Does not affect graphical output.
        """
        if self._video_out is not None:
            self._video_out.release()
            self._video_out = None
        super().wrap_up()
