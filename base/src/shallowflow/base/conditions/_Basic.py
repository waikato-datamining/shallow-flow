from shallowflow.api.condition import AbstractBooleanCondition
from shallowflow.api.config import Option


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


class Not(AbstractBooleanCondition):
    """
    Inverts the result of the base condition.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Inverts the result of the base condition."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("condition", AbstractBooleanCondition, AlwaysFalse(), "The condition to negate"))

    def _do_evaluate(self, o):
        """
        Evaluates the condition.

        :param o: the current object from the owning actor
        :return: the result of the evaluation
        :rtype: bool
        """
        cond = self.get("condition")
        cond.flow_context = self.flow_context
        return not cond.evaluate(o)


class Or(AbstractBooleanCondition):
    """
    Combines the results of the base conditions using OR.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Combines the results of the base conditions using OR."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("conditions", list, list(), "The conditions to combine with OR", base_type=AbstractBooleanCondition))

    def _do_evaluate(self, o):
        """
        Evaluates the condition.

        :param o: the current object from the owning actor
        :return: the result of the evaluation
        :rtype: bool
        """
        conds = self.get("conditions")
        result = False
        for cond in conds:
            cond.flow_context = self.flow_context
            result = result or cond.evaluate(o)
        return result


class And(AbstractBooleanCondition):
    """
    Combines the results of the base conditions using AND.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Combines the results of the base conditions using AND."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("conditions", list, list(), "The conditions to combine with AND", base_type=AbstractBooleanCondition))

    def _do_evaluate(self, o):
        """
        Evaluates the condition.

        :param o: the current object from the owning actor
        :return: the result of the evaluation
        :rtype: bool
        """
        conds = self.get("conditions")
        result = True
        for cond in conds:
            cond.flow_context = self.flow_context
            if not cond.evaluate(o):
                result = False
                break
        return result
