from shallowflow.api.sink import AbstractSimpleSink


class Null(AbstractSimpleSink):
    """
    Consumes all input without doing anything.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Consumes all input without doing anything."

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        return None
