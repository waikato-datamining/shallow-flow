from shallowflow.api.config import AbstractOptionHandler, optionhandler_to_dict, dict_to_optionhandler
from shallowflow.api.actor import FlowContextHandler
from shallowflow.api.serialization.objects import add_dict_writer, add_dict_reader


class AbstractConversion(AbstractOptionHandler, FlowContextHandler):
    """
    Ancestor for simple type conversions, to be used with the Convert transformer.
    """

    def _initialize(self):
        """
        Performs initializations.
        """
        super()._initialize()
        self._flow_context = None

    @property
    def flow_context(self):
        """
        Returns the owning actor.

        :return: the owning actor
        :rtype: Actor
        """
        return self._flow_context

    @flow_context.setter
    def flow_context(self, a):
        """
        Sets the actor to use as owner.

        :param a: the owning actor
        :type a: Actor
        """
        self._flow_context = a

    def _requires_flow_context(self):
        """
        Returns whether flow context is required.

        :return: True if required
        :rtype: bool
        """
        return False

    def accepts(self):
        """
        Returns the type that the conversion accepts.

        :return: the type
        """
        raise NotImplemented()

    def generates(self):
        """
        Returns the type that the conversion generates.

        :return: the type
        """
        raise NotImplemented()

    def _check(self, o):
        """
        Performs checks before the actual conversion.

        :param o: the object to convert
        :return: None if successful checks, otherwise error message
        """
        if o is None:
            return "No object provided for conversion!"
        if self._requires_flow_context() and (self.flow_context is None):
            return "No flow context set!"
        return None

    def _do_convert(self, o):
        """
        Performs the conversion.

        :param o: the object to convert
        :return: the converted object
        """
        raise NotImplemented()

    def convert(self, o):
        """
        Performs the conversion.

        :param o: the object to convert
        :return: the converted object
        """
        msg = self._check(o)
        if msg is not None:
            raise Exception(msg)
        return self._do_convert(o)


# register reader/writer
add_dict_writer(AbstractConversion, optionhandler_to_dict)
add_dict_reader(AbstractConversion, dict_to_optionhandler)
