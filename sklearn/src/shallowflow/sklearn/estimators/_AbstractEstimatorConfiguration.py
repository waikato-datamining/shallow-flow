from shallowflow.api.config import AbstractOptionHandler, optionhandler_to_dict, dict_to_optionhandler
from shallowflow.api.serialization.objects import add_dict_writer, add_dict_reader
from sklearn.base import BaseEstimator


class AbstractEstimatorConfiguration(AbstractOptionHandler):

    def _check(self):
        """
        Hook method before configuring the estimator.

        :return: None if successful check, otherwise error message
        :rtype: str
        """
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
