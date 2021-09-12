from shallowflow.api.actor import InputConsumer
from shallowflow.api.control import MutableActorHandler, ActorHandlerInfo
from shallowflow.api.compatibility import Unknown
from shallowflow.base.directors import SequentialDirector

STATE_INPUT = "input"


class Sequence(MutableActorHandler, InputConsumer):
    """
    Executes the sub-actors one after the other, with the output of an actor being the input for the next; the first actor must accept input.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Executes the sub-actors one after the other, with the output of an actor being the input for the next; the first actor must accept input."

    def reset(self):
        """
        Resets the state of the actor.
        """
        super().reset()
        self._input = None

    @property
    def actor_handler_info(self):
        """
        Returns meta-info about itself.

        :return: the info
        :rtype: ActorHandlerInfo
        """
        return ActorHandlerInfo(can_contain_standalones=False, can_contain_source=False)

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

    def _new_director(self):
        """
        Returns the director to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, allows_standalones=False, requires_source=False, requires_sink=False)

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        if len(self) == 0:
            return [Unknown]
        else:
            return self.actors[0].accepts()

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
