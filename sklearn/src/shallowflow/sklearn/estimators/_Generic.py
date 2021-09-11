from shallowflow.api.config import Option, class_name_to_type
from sklearn.base import BaseEstimator
from ._AbstractEstimatorConfiguration import AbstractEstimatorConfiguration


class GenericConfiguration(AbstractEstimatorConfiguration):
    """
    Generic estimator configuration, using classname and options for constructor.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Generic estimator configuration, using classname and options for constructor."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("class_name", str, "sklearn.ensemble.RandomForestClassifier", "The class name of the estimator to instantiate."))
        self._option_manager.add(Option("options", dict, dict(), "The dictionary to supply to the constructor of the estimator."))

    def _check(self):
        """
        Hook method before configuring the estimator.

        :return: None if successful check, otherwise error message
        :rtype: str
        """
        result = super()._check()
        if result is None:
            try:
                class_name_to_type(self.get("class_name"))
            except Exception:
                result = self._handle_exception("Failed to instantiate %s: %s" % (self.get("class_name")))
        return result

    def _do_configure(self):
        """
        Performs the actual configuring of the estimator.

        :return: the estimator
        :rtype: BaseEstimator
        """
        cls = class_name_to_type(self.get("class_name"))
        try:
            estimator = cls(**self.get("options"))
            return estimator
        except Exception:
            raise Exception(self._handle_exception("Failed to instantiate %s: %s" % (self.get("class_name"))))
