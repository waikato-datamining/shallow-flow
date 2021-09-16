from shallowflow.api.config import AbstractOptionHandler, optionhandler_to_dict, dict_to_optionhandler
from shallowflow.api.actor import FlowContextHandler
from shallowflow.api.serialization.objects import add_dict_writer, add_dict_reader
from sklearn.base import BaseEstimator


class AbstractEstimatorConfiguration(AbstractOptionHandler, FlowContextHandler):

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
        self.reset()

    def _requires_flow_context(self):
        """
        Returns whether flow context is required.

        :return: True if required
        :rtype: bool
        """
        return False

    def _check(self):
        """
        Hook method before configuring the estimator.

        :return: None if successful check, otherwise error message
        :rtype: str
        """
        if self._requires_flow_context() and (self.flow_context is None):
            return "No flow context set!"
        return None

    def _do_configure(self):
        """
        Performs the actual configuring of the estimator.

        :return: the estimator
        :rtype: BaseEstimator
        """
        raise NotImplemented()

    def configure(self):
        """
        Configures and returns the estimator.

        :return: the estimator
        :rtype: BaseEstimator
        """
        msg = self._check()
        if msg is not None:
            raise Exception(msg)
        return self._do_configure()


# register reader/writer
add_dict_writer(AbstractEstimatorConfiguration, optionhandler_to_dict)
add_dict_reader(AbstractEstimatorConfiguration, dict_to_optionhandler)
