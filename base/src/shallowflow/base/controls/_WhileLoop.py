from shallowflow.api.actor import InputConsumer
from shallowflow.api.control import ActorHandler
from shallowflow.api.config import Option
from shallowflow.api.condition import AbstractBooleanCondition
from shallowflow.base.directors import SequentialDirector
from shallowflow.base.conditions import AlwaysTrue


class WhileLoop(ActorHandler, InputConsumer):
    """
    Encapsulates a complete flow.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Executes the sub-flow as long as the boolean condition evaluates to 'True'."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("condition", AbstractBooleanCondition, AlwaysTrue(), "The boolean condition to use"))

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

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if len(self.actors) > 0:
                if isinstance(self.actors[0], InputConsumer):
                    result = "First sub-actor is not allowed to accept input: %s" % self.actors[0].full_name
        if result is None:
            self.get("condition").owner = self
        return result

    def _new_director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, allows_standalones=True, requires_source=True, requires_sink=False)

    def _can_execute_actors(self):
        """
        Returns whether the sub-actors can be executed.

        :return: True if the sub-actors can be executed
        :rtype: bool
        """
        return (len(self.actors) > 0) \
               and self.get("condition").evaluate(self._input)

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        while self._can_execute_actors() and not self.is_stopped:
            result = self._director.execute(self.actors)
            if result is not None:
                break
        return result
