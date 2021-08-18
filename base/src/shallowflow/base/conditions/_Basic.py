from shallowflow.api.condition import AbstractBooleanCondition


class AlwaysTrue(AbstractBooleanCondition):
    """
    Always returns True.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Always returns True"

    def _do_evaluate(self, o):
        """
        Evaluates the condition.

        :param o: the current object from the owning actor
        :return: the result of the evaluation
        :rtype: bool
        """
        return True


class AlwaysFalse(AbstractBooleanCondition):
    """
    Always returns False.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Always returns False"

    def _do_evaluate(self, o):
        """
        Evaluates the condition.

        :param o: the current object from the owning actor
        :return: the result of the evaluation
        :rtype: bool
        """
        return False
