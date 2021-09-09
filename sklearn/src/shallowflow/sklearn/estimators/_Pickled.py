import os
import pickle
from shallowflow.api.config import Option, get_class_name
from shallowflow.api.io import File
from sklearn.base import BaseEstimator
from ._AbstractEstimatorConfiguration import AbstractEstimatorConfiguration


class PickledEsimatorConfiguration(AbstractEstimatorConfiguration):
    """
    Simply loads an estimator from a pickled file.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Simply loads an estimator from a pickled file."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("model_file", File, File("."), "The pickled file to load the estimator from."))

    def _check(self):
        """
        Hook method before configuring the estimator.

        :return: None if successful check, otherwise error message
        :rtype: str
        """
        result = super()._check()
        if result is None:
            model_file = self.get("model_file")
            if not os.path.exists(model_file):
                result = "Model file does not exist: %s" % model_file
            elif os.path.isdir(model_file):
                result = "Model file points to directory: %s" % model_file
        return result

    def _do_configure(self):
        """
        Performs the actual configuring of the estimator.

        :return: the estimator
        :rtype: BaseEstimator
        """
        model_file = self.get("model_file")
        with open(model_file, "rb") as mf:
            estimator = pickle.load(mf)
            if isinstance(estimator, BaseEstimator):
                return estimator
            else:
                raise Exception("Object in %s is not derived from %s!" % (model_file, get_class_name(BaseEstimator)))
