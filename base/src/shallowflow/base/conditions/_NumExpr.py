import numexpr
from shallowflow.api.config import Option
from shallowflow.api.condition import AbstractBooleanCondition


class NumExpr(AbstractBooleanCondition):
    """
    Evaluates expressions using numexpr.

    https://numexpr.readthedocs.io/projects/NumExpr3/en/latest/
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Evaluates the specified numexpr expression.\n" \
               "https://numexpr.readthedocs.io/projects/NumExpr3/en/latest/"

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("expression", str, "True", "The expression to evaluate (must return a boolean); variables get expanded before evaluation"))

    def _do_evaluate(self, o):
        """
        Evaluates the condition.

        :param o: the current object from the owning actor
        :return: the result of the evaluation
        :rtype: bool
        """
        expr = self.variables.expand(str(self.get("expression")))
        result = bool(numexpr.evaluate(expr))
        return result
