from shallowflow.api.control import MutableActorHandler, AbstractDirector, ActorHandlerInfo
from shallowflow.api.transformer import InputConsumer
from shallowflow.api.compatibility import Unknown, is_compatible

STATE_INPUT = "input"


class BranchDirector(AbstractDirector):
    """
    Director for the Branch actor.
    """

    def _do_execute(self, actors):
        """
        Executes the specified list of actors.

        :param actors: the actors to execute
        :type actors: list
        :return: None if successfully executed, otherwise error message
        :rtype: str
        """
        result = None
        for actor in actors:
            if self.is_stopped:
                break
            if actor.is_skipped:
                continue
            result = actor.execute()
            if result is not None:
                break
        return result


class Branch(MutableActorHandler, InputConsumer):
    """
    Forwards the input data to all of its sub-actors.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Forwards the input data to all of its sub-actors."

    @property
    def actor_handler_info(self):
        """
        Returns meta-info about itself.

        :return: the info
        :rtype: ActorHandlerInfo
        """
        return ActorHandlerInfo(can_contain_standalones=False, can_contain_source=False)

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
        compatible = True
        actors = self.actors
        for i in range(len(actors) - 1):
            actor1 = actors[i]
            if isinstance(actor1, InputConsumer):
                classes = actor1.accepts()
                for n in range(i + 1, len(actors), 1):
                    actor2 = actors[n]
                    if not is_compatible(classes, actor2.accepts()) and not is_compatible(actor2, classes):
                        compatible = False
                        break
            if not compatible:
                break

        if compatible:
            result = [Unknown]
        else:
            result = []

        # gather all common classes
        all = set()
        for i in range(len(actors)):
            actor = actors[i]
            if isinstance(actor, InputConsumer):
                classes = actor.accepts()
                if i == 0:
                    for c in classes:
                        all.add(c)
                else:
                    all = all & set(classes)

        if len(all) > 0:
            result = list(all)

        return result

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if len(self.actors) > 0:
                for actor in self.actors:
                    if not isinstance(actor, InputConsumer):
                        result = "Sub-actor does not accept input: %s" % actor.full_name
        return result

    def _new_director(self):
        """
        Returns the director to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return BranchDirector(self)

    def _can_execute_actors(self):
        """
        Returns whether the sub-actors can be executed.

        :return: True if the sub-actors can be executed
        :rtype: bool
        """
        return len(self.actors) > 0

    def _pre_execute(self):
        """
        Before the actual code gets executed.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super()._pre_execute()
        if len(self.actors) > 0:
            for actor in self.actors:
                actor.input(self._input)
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
        return result

    def _post_execute(self):
        """
        After the actual code got executed.
        """
        self._input = None

    def wrap_up(self):
        """
        For finishing up the execution.
        Does not affect graphical output.
        """
        self._input = None
        super().wrap_up()
