import importlib
from collections import OrderedDict
from datetime import datetime
from .logging import LoggableObject
from .serialization import get_dict_reader, get_dict_writer, add_dict_writer, add_dict_reader, has_dict_reader, has_dict_writer


class Option(object):
    """
    Defines a single option.
    """

    def __init__(self, name, value_type, def_value, help, base_type=None):
        """
        Initializes the item.

        :param name: the name of the item
        :type name: str
        :param value_type: the class of the value
        :type value_type: object
        :param def_value: the default value
        :type def_value: object
        :param help: the help string
        :type help: str
        :param base_type: the base class of the value, in case of lists
        :type base_type: object
        """
        if name == "class":
            raise Exception("Cannot use reserved name: %s" % name)
        self.name = name
        self.value_type = value_type
        self.def_value = def_value
        self.help = help
        self.base_type = base_type

    def __str__(self):
        """
        Returns a string describing the item.

        :return: the string describing the item
        :rtype: str
        """
        return "%s/%s: %s\n   %s" % (self.name, str(self.value_type.__name__), repr(self.def_value), self.help)


class OptionManager(LoggableObject):
    """
    Manages multiple options.
    """

    def __init__(self):
        """
        Initializes the manager.
        """
        self._options = OrderedDict()
        self._values = dict()
        self._to_dict_handlers = dict()
        self._from_dict_handlers = dict()

    def add(self, option):
        """
        Adds the option.

        :param option: the item to add
        :type option: Option
        """
        self._options[option.name] = option

    def options(self):
        """
        Returns all options.

        :return: the options
        :rtype: list
        """
        return self._options.values()

    def has(self, name):
        """
        Returns whether the specified option is specified.

        :param name: the name of the item to look for
        :type name: str
        :return: true if the item is present
        :rtype: bool
        """
        return name in self._options

    def set(self, name, value):
        """
        Sets the config value.

        :param name: the name of the item to update its value for
        :type name: str
        :param value: the new value
        :type value: object
        :return: true if updated successfully, false if unknown option or incompatible type
        :rtype: bool
        """
        if not self.has(name):
            self.log("Invalid option name: %s" % name)
            return False
        if not isinstance(value, self._options[name].value_type):
            self.log("Invalid config type for %s: expected=%s, received=%s" % (name, self._options[name].value_type, type(value)))
            return False
        self._values[name] = value

    def get(self, name):
        """
        Returns the currently stored value or the default value.

        :param name: the name of the value to retrieve
        :type name: str
        :return: the value, None if invalid option name
        :rtype: object
        """
        if not self.has(name):
            return None
        if name in self._values:
            return self._values[name]
        else:
            return self._options[name].def_value

    def reset(self):
        """
        Resets all options to default values.
        """
        self._values.clear()

    def set_to_dict_handler(self, name, handler):
        """
        Sets the read method that handles the specified option.

        :param name: the name of the option to handle
        :type name: str
        :param handler: the handler function
        """
        self._to_dict_handlers[name] = handler

    def has_to_dict_handler(self, name):
        """
        Checks whether a read handler is set for the option.

        :param name: the name of the option
        :type name: str
        :return: true if a handler method registered
        :rtype: bool
        """
        return name in self._to_dict_handlers

    def get_to_dict_handler(self, name):
        """
        Returns the handler registered for the option.

        :param name: the name of the option
        :type name: str
        :return: the handler, None if no handler registered
        """
        if not self.has_to_dict_handler(name):
            return None
        else:
            return self._to_dict_handlers[name]

    def set_from_dict_handler(self, name, handler):
        """
        Sets the write method that handles the specified option.

        :param name: the name of the option to handle
        :type name: str
        :param handler: the handler function
        """
        self._from_dict_handlers[name] = handler

    def has_from_dict_handler(self, name):
        """
        Checks whether a write handler is set for the option.

        :param name: the name of the option
        :type name: str
        :return: true if a handler method registered
        :rtype: bool
        """
        return name in self._from_dict_handlers

    def get_from_dict_handler(self, name):
        """
        Returns the handler registered for the option.

        :param name: the name of the option
        :type name: str
        :return: the handler, None if no handler registered
        """
        if not self.has_from_dict_handler(name):
            return None
        else:
            return self._from_dict_handlers[name]

    def from_dict(self, d):
        """
        Sets all the values from the dictionary.

        :param d: the dictionary to get the values from
        :type d: dict
        """
        for k in d:
            if k not in self._options:
                self.log("Unknown option: %s/%s" % (k, d[k]))
                continue

            # was a base type define for the elements of the list?
            if isinstance(d[k], list) and (self._options[k].base_type is not None):
                if has_dict_reader(self._options[k].base_type):
                    reader = get_dict_reader(self._options[k].base_type)
                    l = []
                    for item in d[k]:
                        l.append(reader(item))
                    self.set(k, l)
                    continue

            # special handler registered?
            if self.has_from_dict_handler(k):
                handler = self.get_from_dict_handler(k)
                self.set(k, handler(d[k]))
                continue

            # reader registered for type?
            if has_dict_reader(self._options[k].value_type):
                reader = get_dict_reader(self._options[k].value_type)
                self.set(k, reader(d[k]))

            self.set(k, d[k])

    def to_dict(self, skip_default=False):
        """
        Returns all the options as dictionary.

        :param skip_default: if enabled, skips values that are default ones
        :type skip_default: bool
        :return: the options as dictionary
        :rtype: dict
        """
        result = dict()
        for k in self._options:
            if isinstance(self.get(k), list) and (self._options[k].base_type is not None):
                if has_dict_writer(self._options[k].base_type):
                    writer = get_dict_writer(self._options[k].base_type)
                    l = []
                    for item in self.get(k):
                        l.append(writer(item))
                    result[k] = l
                    continue

            # special handler registered?
            if self.has_to_dict_handler(k):
                handler = self.get_to_dict_handler(k)
                result[k] = handler(self.get(k))
                continue

            # writer registered for type?
            if has_dict_writer(self._options[k].value_type):
                writer = get_dict_writer(self._options[k].value_type)
                result[k] = writer(self.get(k))
                continue

            if not skip_default or (self.get(k) != self._options[k].def_value):
                result[k] = self.get(k)
        return result

    def to_help(self):
        """
        Generates a simple help string for all the options.

        :return: the generated helps tring
        :rtype: str
        """
        result = ""
        for item in self.options():
            if len(result) > 0:
                result += "\n"
            result += str(item)
        return result


class AbstractOptionHandler(LoggableObject):
    """
    The ancestor for all classes that handle options.
    """

    def __init__(self):
        """
        Initializes the object.
        """
        self.initialize()
        self.reset()

    def initialize(self):
        """
        Performs initializations.
        """
        self._option_manager = OptionManager()
        self._option_manager.add(Option("debug", bool, False, "If enabled, outputs some debugging information"))
        self._log_prefix = type(self).__name__

    def reset(self):
        """
        Resets the state of the object.
        """
        pass

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
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
    def is_debug(self):
        """
        Returns whether debug mode is on.

        :return: true if on
        :rtype: bool
        """
        return self.get("debug")

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

    def _get_log_prefix(self):
        """
        Returns the log prefix for this object.

        :return: the prefix
        :rtype: str
        """
        return self._log_prefix

    @property
    def log_prefix(self):
        """
        Returns the log prefix for this object.

        :return: the prefix
        :rtype: str
        """
        return self._get_log_prefix()

    def log(self, *args):
        """
        Logs the arguments.

        :param args: the arguments to log
        """
        print(*("%s - %s -" % (self.log_prefix, str(datetime.now())), *args))

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



def dict_to_optionhandler(d):
    """
    Turns the dictionary into an option handler.

    :param d: the dictionary describing the actor
    :type d: dict
    :return: the option handler
    :rtype: AbstractOptionHandler
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


def optionhandler_to_dict(a):
    """
    Turns the option handler into a dictionary describing it.

    :param a: the option handler to convert
    :type a: AbstractOptionHandler
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
add_dict_writer(AbstractOptionHandler, optionhandler_to_dict)
add_dict_reader(AbstractOptionHandler, dict_to_optionhandler)
