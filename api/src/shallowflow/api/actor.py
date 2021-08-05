import importlib
import traceback
import shallowflow.api.serialization as serialization
from .config import Option, OptionManager
from .logging import LoggableObject


class Actor(LoggableObject):
    """
    The ancestor for all actors.
    """

    def __init__(self):
        """
        Initializes the actor.
        """
        self.initialize()
        self.reset()

    def initialize(self):
        """
        Performs initializations.
        """
        self._option_manager = OptionManager()
        self._option_manager.add(Option("debug", bool, False, "If enabled, outputs some debugging information"))
        self._parent = None

    def reset(self):
        """
        Resets the state of the actor.
        """
        pass

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "-description missing-"

    @property
    def option_manager(self):
        """
        Returns the option manager.

        :return: the manager
        :rtype: OptionManager
        """
        return self._option_manager

    @property
    def options(self):
        """
        Returns the current options.

        :return: the current options
        :rtype: dict
        """
        return self._option_manager.to_dict()

    @options.setter
    def options(self, d):
        """
        Sets the options to use.

        :param d: the options to set
        :type d: dict
        """
        if d is None:
            d = dict()
        self._option_manager.from_dict(d)
        self.reset()

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

    def get(self, name):
        """
        Returns the value for the specified option.

        :param name: the name of the option to retrieve
        :type name: str
        :return: the value of the option, None if invalid option
        """
        return self._option_manager.get(name)

    def set(self, name, value):
        """
        Sets the value for the specified option.

        :param name: the name of the option to set
        :type name: str
        :param value: the value of the option to set
        :type value: object
        """
        self._option_manager.set(name, value)

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
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

    def to_help(self):
        """
        Outputs a simple help string.

        :return: the generated help string.
        :rtype: str
        """
        return type(self).__name__ + "\n" \
               + "=" * (len(type(self).__name__)) + "\n\n" \
               + self.description() + "\n\n" \
               + self._option_manager.to_help() + "\n"


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


def dict_to_actor(d):
    """
    Turns the dictionary into an actor.

    :param d: the dictionary describing the actor
    :type d: dict
    :return: the actor
    :rtype: Actor
    """
    Cls = getattr(importlib.import_module(d["module"]), d["class"])
    result = Cls()
    result.options = d["options"]
    return result


def actor_to_dict(a):
    """
    Turns the actor into a dictionary describing it.

    :param a: the actor to convert
    :type a: Actor
    :return: the generated dictionary
    :rtype: dict
    """
    result = dict()
    m = type(a).__module__
    c = type(a).__name__
    if m.split(".")[-1].startswith("_"):
        try:
            m_short = ".".join(m.split(".")[:-1])
            getattr(importlib.import_module(m_short), c)
            m = m_short
        except:
            pass
    result["module"] = m
    result["class"] = c
    result["options"] = a.options
    return result


# register reader/writer
serialization.add_dict_writer(Actor, actor_to_dict)
serialization.add_dict_reader(Actor, dict_to_actor)
