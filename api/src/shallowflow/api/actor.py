import traceback
from .config import ConfigItem, ConfigManager
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
        self._configmanager = ConfigManager()
        self._configmanager.add(ConfigItem("debug", bool, False, "If enabled, outputs some debugging information"))

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
    def configmanager(self):
        """
        Returns the config manager.

        :return: the manager
        :rtype: ConfigManager
        """
        return self._configmanager

    @property
    def config(self):
        """
        Returns the current configuration.

        :return: the configuration
        :rtype: dict
        """
        return self._configmanager.to_dict()

    @config.setter
    def config(self, config):
        """
        Sets the configuration to use.

        :param config: the configuration
        :type config: dict
        """
        if config is None:
            config = dict()
        self._configmanager.from_dict(config)
        self.reset()

    def get(self, name):
        """
        Returns the value for the specified option.

        :param name: the name of the option to retrieve
        :type name: str
        :return: the value of the option, None if invalid option
        """
        return self._configmanager.get(name)

    def set(self, name, value):
        """
        Sets the value for the specified option.

        :param name: the name of the option to set
        :type name: str
        :param value: the value of the option to set
        :type value: object
        """
        self._configmanager.set(name, value)

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if sucessful, otherwise error message
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
               + self._configmanager.to_help() + "\n"


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
