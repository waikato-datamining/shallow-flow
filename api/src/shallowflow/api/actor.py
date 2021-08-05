import importlib
import traceback
import shallowflow.api.serialization as serialization
from datetime import datetime
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
        self._option_manager.add(Option("name", str, "", "The name to use for this actor, leave empty for class name"))
        self._parent = None
        self._log_prefix = None

    def reset(self):
        """
        Resets the state of the actor.
        """
        self._log_prefix = None

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
        return self._option_manager.to_dict(skip_default=True)

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

    @property
    def is_debug(self):
        """
        Returns whether debug mode is on.

        :return: true if on
        :rtype: bool
        """
        return self.get("debug")

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

    @property
    def log_prefix(self):
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

    def log(self, *args):
        """
        Logs the arguments.

        :param args: the arguments to log
        """
        print(*("%s - %s -" % (self.log_prefix, str(datetime.now())), *args))

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
    p = d["class"].split(".")
    m = ".".join(p[:-1])
    c = p[-1]
    Cls = getattr(importlib.import_module(m), c)
    result = Cls()
    if "options" in d:
        result.options = d["options"]
    else:
        result.options = dict()
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
    # can we make the module nicer, by dropping the _CLASS part?
    if m.split(".")[-1].startswith("_"):
        try:
            m_short = ".".join(m.split(".")[:-1])
            getattr(importlib.import_module(m_short), c)
            m = m_short
        except:
            pass
    result["class"] = m + "." + c
    options = a.options
    if len(options) != 0:
        result["options"] = a.options
    return result


# register reader/writer
serialization.add_dict_writer(Actor, actor_to_dict)
serialization.add_dict_reader(Actor, dict_to_actor)
