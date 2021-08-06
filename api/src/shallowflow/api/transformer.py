from .actor import InputConsumer, OutputProducer


class AbstractSimpleTransformer(InputConsumer, OutputProducer):
    """
    Ancestor for simple source actors.
    """

    def initialize(self):
        """
        Performs initializations.
        """
        super(AbstractSimpleTransformer, self).initialize()
        self._output = list()
        self._input = None

    def reset(self):
        """
        Resets the state of the actor.
        """
        super(AbstractSimpleTransformer, self).reset()
        self._output = list()
        self._input = None

    def input(self, data):
        """
        Sets the input data to consume.

        :param data: the data to consume
        :type data: object
        """
        self._input = data

    def _pre_execute(self):
        """
        Before the actual code gets executed.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super()._pre_execute()
        if result is None:
            self._output.clear()
        return result

    def _post_execute(self):
        """
        After the actual code got executed.
        """
        self._input = None

    def has_output(self):
        """
        Returns whether output data is available.

        :return: true if available
        :rtype: bool
        """
        return len(self._output) > 0

    def output(self):
        """
        Returns the next output data.

        :return: the data, None if nothing available
        :rtype: object
        """
        result = None
        if len(self._output) > 0:
            result = self._output[0]
            del self._output[0]
        return result

    def wrap_up(self):
        """
        For finishing up the execution.
        Does not affect graphical output.
        """
        self._input = None
        self._output = None
        super().wrap_up()
