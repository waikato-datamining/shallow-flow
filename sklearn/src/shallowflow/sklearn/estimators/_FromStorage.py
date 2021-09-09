from shallowflow.api.config import Option, get_class_name
from shallowflow.api.storage import is_valid_name
from sklearn.base import BaseEstimator
from ._AbstractEstimatorConfiguration import AbstractEstimatorConfiguration


class FromStorageConfiguration(AbstractEstimatorConfiguration):
    """
    Retrieves the estimator from storage.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Retrieves the estimator from storage."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="storage_name", value_type=str, def_value="storage",
                                        help="The name of the storage item to retrieve"))

    def _check(self):
        """
        Hook method before configuring the estimator.

        :return: None if successful check, otherwise error message
        :rtype: str
        """
        result = super()._check()
        if result is None:
            name = self.get("storage_name")
            if len(name) == 0:
                result = "No storage name provided!"
            elif not is_valid_name(name):
                result = "Not a valid storage name: %s" % name
            elif not self.owner.storage_handler.storage.has(name):
                result = "Storage item not present: %s" % name
        return result

    def _do_configure(self):
        """
        Performs the actual configuring of the estimator.

        :return: the estimator
        :rtype: BaseEstimator
        """
        name = self.get("storage_name")
        estimator = self.owner.storage_handler.storage.get(name)
        if isinstance(estimator, BaseEstimator):
            return estimator
        else:
            raise Exception("Storage item %s is not derived from %s, but an instance of %s!" % (name, get_class_name(BaseEstimator), get_class_name(estimator)))
