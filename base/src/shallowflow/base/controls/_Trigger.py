from shallowflow.api.condition import AbstractBooleanCondition
from shallowflow.api.config import Option
from shallowflow.api.control import ActorHandler
from shallowflow.api.transformer import InputConsumer, OutputProducer
from shallowflow.base.directors import SequentialDirector
from shallowflow.base.conditions import AlwaysTrue


class AbstractTrigger(ActorHandler, InputConsumer, OutputProducer):
    """
    Ancestor for Tee-like control actors.
    """

    def reset(self):
        """
        Resets the state of the actor.
        """
        super().reset()
        self._output = None
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
        return result

    def _pre_execute(self):
        """
        Before the actual code gets executed.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super()._pre_execute()
        if result is None:
            self._output = None
        return result

    def _new_director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        raise NotImplemented()

    def _can_execute_actors(self):
        """
        Returns whether the sub-actors can be executed.

        :return: True if the sub-actors can be executed
        :rtype: bool
        """
        return len(self.actors) > 0

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        if self._can_execute_actors():
            result = self._director.execute(self.actors)
        if result is None:
            self._output = self._input
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
        return self._output is not None

    def output(self):
        """
        Returns the next output data.

        :return: the data, None if nothing available
        :rtype: object
        """
        result = None
        if self._output is not None:
            result = self._output
            self._output = None
        return result

    def wrap_up(self):
        """
        For finishing up the execution.
        Does not affect graphical output.
        """
        self._input = None
        self._output = None
        super().wrap_up()


class Trigger(AbstractTrigger):
    """
    Executes the sub-flow whenever data arrives before forwarding it.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Executes the sub-flow whenever data arrives before forwarding it."

    def _new_director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, allows_standalones=True, requires_source=True, requires_sink=False)


class ConditionalTrigger(AbstractTrigger):
    """
    Executes the sub-flow whenever a token arrives before forwarding it only if the boolean condition evaluates to 'True'
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Executes the sub-flow whenever a token arrives before forwarding it only if the boolean condition evaluates to 'True'."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("condition", AbstractBooleanCondition, AlwaysTrue(), "The boolean condition to use"))

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            self.get("condition").owner = self
        return result

    def _new_director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, allows_standalones=False, requires_source=False, requires_sink=False)

    def _can_execute_actors(self):
        """
        Returns whether the sub-actors can be executed.

        :return: True if the sub-actors can be executed
        :rtype: bool
        """
        result = super()._can_execute_actors()
        if result:
            result = self.get("condition").evaluate(self._input)
        return result
