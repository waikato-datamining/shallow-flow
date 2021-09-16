from shallowflow.api.condition import AbstractBooleanCondition
from shallowflow.api.config import Option
from shallowflow.api.control import MutableActorHandler, ActorHandlerInfo
from shallowflow.api.transformer import InputConsumer, OutputProducer
from shallowflow.api.compatibility import Unknown
from shallowflow.base.directors import SequentialDirector
from shallowflow.base.conditions import AlwaysTrue

STATE_INPUT = "input"


class AbstractTee(MutableActorHandler, InputConsumer, OutputProducer):
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

    def _backup_state(self):
        """
        For backing up the internal state before reconfiguring due to variable changes.

        :return: the state dictionary
        :rtype: dict
        """
        result = super()._backup_state()
        if self._input is not None:
            result[STATE_INPUT] = self._input
        return result

    def _restore_state(self, state):
        """
        Restores the state from the state dictionary after being reconfigured due to variable changes.

        :param state: the state dictionary to use
        :type state: dict
        """
        if STATE_INPUT in state:
            self._input = state[STATE_INPUT]
            del state[STATE_INPUT]
        super()._restore_state(state)

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
        Returns the director to use for executing the actors.

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
        raise NotImplemented()

    def _post_execute(self):
        """
        After the actual code got executed.
        """
        self._input = None
        if self.is_stopped:
            self._output = None
        super()._post_execute()

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


class Tee(AbstractTee):
    """
    Forwards the incoming data to the defined sub-flow before forwarding it.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Forwards the incoming data to the defined sub-flow before forwarding it."

    def _new_director(self):
        """
        Returns the director to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, allows_standalones=False, requires_source=False, requires_sink=False)

    @property
    def actor_handler_info(self):
        """
        Returns meta-info about itself.

        :return: the info
        :rtype: ActorHandlerInfo
        """
        return ActorHandlerInfo(can_contain_standalones=False, can_contain_source=False)

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
                if not isinstance(self.actors[0], InputConsumer):
                    result = "First sub-actor does not accept input: %s" % self.actors[0].full_name
        return result

    def _pre_execute(self):
        """
        Before the actual code gets executed.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super()._pre_execute()
        if len(self.actors) > 0:
            self.actors[0].input(self._input)
        return result

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


class ConditionalTee(Tee):
    """
    Forwards the incoming data to the defined sub-flow before forwarding it only if the boolean condition evaluates to 'True'
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Forwards the incoming data to the defined sub-flow before forwarding it only if the boolean condition evaluates to 'True'."

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
