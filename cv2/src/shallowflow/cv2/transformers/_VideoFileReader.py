import cv2
from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.config import Option

STATE_CAP = "cap"
STATE_FRAME_COUNT = "frame_count"
STATE_FRAMES_PROCESSED = "frames_processed"


class VideoFileReader(AbstractSimpleTransformer):
    """
    Outputs frames from the video file that it received.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Outputs frames from the video file that it received."

    def _initialize(self):
        """
        Performs initializations.
        """
        super()._initialize()
        self._cap = None
        self._frame_count = 0
        self._frames_processed = 0

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="nth_frame", value_type=int, def_value=1,
                                        help="Forward only every nth frame."))
        self._option_manager.add(Option(name="max_frames", value_type=int, def_value=-1,
                                        help="The maximum number of frames to forward; <=0 for no limit."))

    def _backup_state(self):
        """
        For backing up the internal state before reconfiguring due to variable changes.

        :return: the state dictionary
        :rtype: dict
        """
        result = super()._backup_state()
        if self._cap is not None:
            result[STATE_CAP] = self._cap
        result[STATE_FRAME_COUNT] = self._frame_count
        result[STATE_FRAMES_PROCESSED] = self._frames_processed
        return result

    def _restore_state(self, state):
        """
        Restores the state from the state dictionary after being reconfigured due to variable changes.

        :param state: the state dictionary to use
        :type state: dict
        """
        if STATE_CAP in state:
            self._cap = state[STATE_CAP]
            del state[STATE_CAP]

        self._frame_count = state[STATE_FRAME_COUNT]
        del state[STATE_FRAME_COUNT]

        self._frames_processed = state[STATE_FRAMES_PROCESSED]
        del state[STATE_FRAMES_PROCESSED]

        super()._restore_state(state)

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if self.get("nth_frame") < 1:
                result = "nth_frame must be at least 1!"
        return result

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        try:
            self._cap = cv2.VideoCapture(self._input)
            self._frame_count = 0
            self._frames_processed = 0
        except Exception:
            result = self._handle_exception("Failed to open video file: %s" % str(self._input))
        return result

    def _close_video(self):
        """
        Closes the video stream.
        """
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None

    def has_output(self):
        """
        Returns whether output data is available.

        :return: always True
        :rtype: bool
        """
        if len(self._output) > 0:
            return True

        if self._cap is not None:
            max_frames = self.get("max_frames")
            try:
                while self._cap.isOpened():
                    retval, frame = self._cap.read()
                    if not retval:
                        self._close_video()
                        break
                    else:
                        self._frame_count += 1
                        if self._frame_count % self.get("nth_frame") == 0:
                            self._frames_processed += 1
                            self._output.append(frame)
                            if (max_frames > 0) and (self._frames_processed >= max_frames):
                                self._close_video()
                                break
                        else:
                            continue
            except:
                self._handle_exception("Failed to read next frame!")
                return False

        if len(self._output) > 0:
            return True
        else:
            return False
