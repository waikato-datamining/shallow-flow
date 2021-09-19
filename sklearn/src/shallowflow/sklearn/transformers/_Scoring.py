from shallowflow.api.config import Option
from shallowflow.api.storage import StorageUser, StorageName
from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.sklearn.containers import EstimatorContainer, EstimatorPredictions
from shallowflow.sklearn.datasets import Dataset


class AbstractScoring(AbstractSimpleTransformer, StorageUser):
    """
    Ancestor for classes that perform scoring on incoming data and
    an estimator from storage.
    """

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="storage_name", value_type=StorageName, def_value=StorageName("storage"),
                                        help="The name of the storage item that represents the estimator or estimator container"))

    @property
    def uses_storage(self):
        """
        Returns whether storage is used.

        :return: True if used
        :rtype: bool
        """
        return not self.is_skipped

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [Dataset]

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [EstimatorPredictions]

    def setup(self):
        """
        Prepares the actor for use.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = super().setup()
        if result is None:
            if self.storage_handler is None:
                result = "No storage handler available!"
        if result is None:
            if len(self.get("storage_name")) == 0:
                result = "No storage name provided!"
        return result


class SupervisedScoring(AbstractScoring):
    """
    Applies the supervised estimator from storage to the incoming dataset.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Applies the supervised estimator from storage to the incoming dataset."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("predictions", bool, True, "Whether to generate predictions"))
        self._option_manager.add(Option("probabilities", bool, False, "Whether to generate probabilities"))

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None

        estimator = self.storage_handler.storage.get(self.get("storage_name"))
        if isinstance(estimator, EstimatorContainer):
            estimator = estimator.get(EstimatorContainer.VALUE_ESTIMATOR)
        dataset = self._input
        try:
            preds = None
            probs = None
            if self.get("predictions"):
                preds = estimator.predict(dataset.X)
            if self.get("probabilities"):
                probs = estimator.predict_proba(dataset.X)
            self._output.append(EstimatorPredictions(estimator, predictions=preds, probabilities=probs, dataset=dataset))
        except Exception:
            result = self._handle_exception("Failed to configure estimator!")

        return result


class UnsupervisedScoring(AbstractScoring):
    """
    Applies the unsupervised estimator from storage to the incoming dataset.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Applies the unsupervised estimator from storage to the incoming dataset."

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None

        estimator = self.storage_handler.storage.get(self.get("storage_name"))
        if isinstance(estimator, EstimatorContainer):
            estimator = estimator.get(EstimatorContainer.VALUE_ESTIMATOR)
        dataset = self._input
        try:
            preds = estimator.predict(dataset.X)
            self._output.append(EstimatorPredictions(estimator, predictions=preds, dataset=dataset))
        except Exception:
            result = self._handle_exception("Failed to configure estimator!")

        return result
