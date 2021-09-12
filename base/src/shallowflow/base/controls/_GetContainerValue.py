from shallowflow.api.actor import InputConsumer
from shallowflow.api.config import Option, get_class_name
from shallowflow.api.container import AbstractContainer
from shallowflow.api.control import ActorHandlerInfo
from shallowflow.base.directors import SequentialDirector
from ._Tee import AbstractTee


class GetContainerValue(AbstractTee):
    """
    Lets the user obtain a value from a container passing through.
    Can either be processed in a sub-flow or by the following actor(s).
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Lets the user obtain a value from a container passing through.\n" \
               + "Can either be processed in a sub-flow or by the following actor(s)."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self.option_manager.add(Option(name="value_name", value_type=str, def_value="",
                                       help="The value to obtain from the container"))
        self.option_manager.add(Option(name="switch_outputs", value_type=bool, def_value=False,
                                       help="Whether to forward the value to the following actor rather than the sub-flow."))
        self.option_manager.add(Option(name="ignore_missing", value_type=bool, def_value=False,
                                       help="Whether to ignore missing container values or generate an error"))

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

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if len(self.get("value_name")) == 0:
                result = "No value name provided!"
        return result

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None

        if not isinstance(self._input, AbstractContainer):
            result = "Input is not a container, but: %s" % get_class_name(self._input)

        name = self.get("value_name")
        if result is None:
            if not self._input.has(name):
                msg = "Value not found in container: %s" % name
                if self.get("ignore_missing"):
                    self.log(msg)
                else:
                    result = msg

        if result is None:
            value = self._input.get(name)
            if self.get("switch_outputs"):
                subflow = self._input
                forward = value
            else:
                subflow = value
                forward = self._input
            if len(self.actors) > 0:
                self.actors[0].input(subflow)
            if self._can_execute_actors():
                result = self._director.execute(self.actors)
            if result is None:
                self._output = forward

        return result
