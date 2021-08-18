from .actor import InputConsumer


class AbstractSimpleSink(InputConsumer):
    """
    Ancestor for simple source actors.
    """

    def initialize(self):
        """
        Performs initializations.
        """
        super().initialize()
        self._input = None

    def reset(self):
        """
        Resets the state of the actor.
        """
        super().reset()
        self._input = None

    def input(self, data):
        """
        Sets the input data to consume.

        :param data: the data to consume
        :type data: object
        """
        self._input = data

    def _post_execute(self):
        """
        After the actual code got executed.
        """
        self._input = None
