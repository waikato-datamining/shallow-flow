from shallowflow.api.source import AbstractSimpleSource


class Start(AbstractSimpleSource):
    """
    Outputs dummy data to execute the next actor.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Outputs dummy data to execute the next actor."

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._output.append("start")
        return None
