from shallowflow.api.condition import AbstractBooleanCondition
from shallowflow.api.config import Option
from shallowflow.api.control import ActorHandlerInfo
from shallowflow.api.compatibility import Unknown
from shallowflow.api.transformer import InputConsumer
from shallowflow.base.directors import SequentialDirector
from shallowflow.base.conditions import AlwaysTrue
from shallowflow.base.controls import AbstractTee


class Trigger(AbstractTee):
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
        Returns the director to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, allows_standalones=True, requires_source=True, requires_sink=False)

    @property
    def actor_handler_info(self):
        """
        Returns meta-info about itself.

        :return: the info
        :rtype: ActorHandlerInfo
        """
        return ActorHandlerInfo(can_contain_standalones=True, can_contain_source=True)

    def _check_actors(self, actors):
        """
        Performs checks on the sub-actors.

        :param actors: the actors to check
        :type actors: list
        :return: None if successful check, otherwise error message
        :rtype: str
        """
        result = super()._check_actors(actors)
        if result is None:
            if len(self.actors) > 0:
                if isinstance(self.actors[0], InputConsumer):
                    result = "First sub-actor is not allowed to accept input: %s" % self.actors[0].full_name
        return result

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [Unknown]

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [Unknown]

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


class ConditionalTrigger(Trigger):
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
            self.get("condition").flow_context = self
        return result

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
