from shallowflow.api.control import MutableActorHandler, AbstractDirector
from shallowflow.api.transformer import InputConsumer


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
                for actor in self.actors:
                    if not isinstance(actor, InputConsumer):
                        result = "Sub-actor does not accept input: %s" % actor.full_name
        return result

    def _new_director(self):
        """
        Returns the directory to use for executing the actors.

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
