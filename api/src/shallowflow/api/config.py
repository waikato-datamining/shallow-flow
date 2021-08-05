from collections import OrderedDict
from .logging import LoggableObject


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
        return "%s/%s: %s\n   %s" % (self.name, str(self.value_type.__name__), str(self.def_value), self.help)


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
            if self.has_from_dict_handler(k):
                handler = self.get_from_dict_handler(k)
                self.set(k, handler(d[k]))
            else:
                self.set(k, d[k])

    def to_dict(self):
        """
        Returns all the options as dictionary.

        :return: the options as dictionary
        :rtype: dict
        """
        result = dict()
        for k in self._options:
            if self.has_to_dict_handler(k):
                handler = self.get_to_dict_handler(k)
                result[k] = handler(self.get(k))
            else:
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
