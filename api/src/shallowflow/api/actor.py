import traceback
import shallowflow.api.serialization as serialization
from .config import Option, AbstractOptionHandler, dict_to_optionhandler, optionhandler_to_dict


class Actor(AbstractOptionHandler):
    """
    The ancestor for all actors.
    """

    def initialize(self):
        """
        Performs initializations.
        """
        super().initialize()
        self._option_manager.add(Option("name", str, "", "The name to use for this actor, leave empty for class name"))
        self._parent = None
        self._stopped = False

    def reset(self):
        """
        Resets the state of the object.
        """
        super().reset()
        self._log_prefix = None

    @property
    def parent(self):
        """
        Returns the current parent actor.

        :return: the parent actor
        :rtype: Actor
        """
        return self._parent

    @parent.setter
    def parent(self, a):
        """
        Sets the actor to use as parent.

        :param a: the parent actor
        :type a: Actor
        """
        self._parent = a
        self.reset()

    @property
    def root(self):
        """
        Returns the root actor.

        :return: the root actor, None if not available
        :rtype: Actor
        """
        if self._parent is not None:
            return self._parent.root
        else:
            return self

    @property
    def name(self):
        """
        Returns the stored name or the class name.

        :return: the name
        :rtype: str
        """
        if len(self.get("name")) == 0:
            return type(self).__name__
        else:
            return self.get("name")

    @property
    def full_name(self):
        """
        Returns the full path of the actor.

        :return: the path
        :rtype: str
        """
        return self._get_log_prefix()

    def _get_log_prefix(self):
        """
        Returns the log prefix for this actor.

        :return: the prefix
        :rtype: str
        """
        if self._log_prefix is None:
            if self.parent is not None:
                prefix = self.parent.log_prefix + "."
            else:
                prefix = ""
            prefix += self.name
            self._log_prefix = prefix
        return self._log_prefix

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        self._stopped = False
        return None

    def _pre_execute(self):
        """
        Before the actual code gets executed.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        return None

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
        pass

    def execute(self):
        """
        Executes the actor
        :return:
        """
        try:
            result = self._pre_execute()
            if result is None:
                result = self._do_execute()
                self._post_execute()
        except Exception:
            result = traceback.format_exc()
        return result

    def wrap_up(self):
        """
        For finishing up the execution.
        Does not affect graphical output.
        """
        pass

    def clean_up(self):
        """
        Also cleans up graphical output.
        """
        pass

    def stop_execution(self):
        """
        Stops the actor execution.
        """
        self._stopped = True
        if self.is_debug:
            self.log("Stopped!")

    @property
    def is_stopped(self):
        """
        Returns whether the actor was stopped.

        :return: true if stopped
        :rtype: bool
        """
        return self._stopped


class InputConsumer(Actor):
    """
    Interface for actors that consume input.
    """

    def input(self, data):
        """
        Sets the input data to consume.

        :param data: the data to consume
        :type data: object
        """
        raise NotImplemented()


class OutputProducer(Actor):
    """
    Interface for actors that generate output.
    """

    def output(self):
        """
        Returns the next output data.

        :return: the data, None if nothing available
        :rtype: object
        """
        raise NotImplemented()

    def has_output(self):
        """
        Returns whether output data is available.

        :return: true if available
        :rtype: bool
        """
        raise NotImplemented()


def is_source(actor):
    """
    Checks whether the actor is a source.

    :param actor: the actor to check
    :type actor: Actor
    :return: true if a source actor
    """
    return isinstance(actor, OutputProducer) and not isinstance(actor, InputConsumer)


def is_transformer(actor):
    """
    Checks whether the actor is a transformer.

    :param actor: the actor to check
    :type actor: Actor
    :return: true if a transformer actor
    """
    return isinstance(actor, OutputProducer) and isinstance(actor, InputConsumer)


def is_sink(actor):
    """
    Checks whether the actor is a sink.

    :param actor: the actor to check
    :type actor: Actor
    :return: true if a sink actor
    """
    return not isinstance(actor, OutputProducer) and isinstance(actor, InputConsumer)


# register reader/writer
serialization.add_dict_writer(Actor, optionhandler_to_dict)
serialization.add_dict_reader(Actor, dict_to_optionhandler)
