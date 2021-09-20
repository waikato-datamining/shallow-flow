from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.config import Option
from shallowflow.sklearn.estimators import AbstractEstimatorConfiguration
from shallowflow.sklearn.estimators import GenericConfiguration
from shallowflow.sklearn.datasets import Dataset, SupervisedDataset
from shallowflow.sklearn.containers import EstimatorContainer
from sklearn.base import BaseEstimator


class AbstractTrainEstimator(AbstractSimpleTransformer):
    """
    Trains the specified sklearn estimator on the incoming dataset.
    """

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option(name="estimator", value_type=AbstractEstimatorConfiguration, def_value=self._get_default_estimator(),
                                        help="The estimator configuration to use"))

    def _get_default_estimator(self):
        """
        Returns the default estimator config to use.

        :return: the estimator
        :rtype: AbstractEstimatorConfiguration
        """
        raise NotImplemented()

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [EstimatorContainer]

    def _do_train(self, estimator, dataset):
        """
        Trains the estimator and returns the container.

        :param estimator: the estimator to train
        :type estimator: BaseEstimator
        :param dataset: the dataset to train with
        :type dataset: Dataset
        :return: the generated container if successfully trained
        :rtype: EstimatorContainer
        """
        raise NotImplemented()

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None

        try:
            config = self.get("estimator")
            config.flow_context = self
            estimator = config.configure()
        except Exception:
            result = self._handle_exception("Failed to configure estimator!")

        if result is None:
            try:
                cont = self._do_train(estimator, self._input)
                if cont is not None:
                    self._output.append(cont)
            except Exception:
                result = self._handle_exception("Failed to train estimator!")

        return result


class TrainSupervisedEstimator(AbstractTrainEstimator):
    """
    Trains the specified sklearn classifier on the incoming dataset.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Trains the specified sklearn estimator on the incoming dataset."

    def _get_default_estimator(self):
        """
        Returns the default estimator config to use.

        :return: the estimator
        :rtype: AbstractEstimatorConfiguration
        """
        return GenericConfiguration({"class_name": ""})

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [SupervisedDataset]

    def _do_train(self, estimator, dataset):
        """
        Trains the estimator and returns the container.

        :param estimator: the estimator to train
        :type estimator: BaseEstimator
        :param dataset: the dataset to train with
        :type dataset: Dataset
        :return: the generated container if successfully trained
        :rtype: EstimatorContainer
        """
        estimator.fit(dataset.X, dataset.y)
        return EstimatorContainer(estimator=estimator, dataset=dataset)


class TrainUnsupervisedEstimator(AbstractTrainEstimator):
    """
    Trains the specified sklearn classifier on the incoming dataset.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Trains the specified sklearn estimator on the incoming dataset."

    def _get_default_estimator(self):
        """
        Returns the default estimator config to use.

        :return: the estimator
        :rtype: AbstractEstimatorConfiguration
        """
        return GenericConfiguration({"class_name": ""})

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [Dataset]

    def _do_train(self, estimator, dataset):
        """
        Trains the estimator and returns the container.

        :param estimator: the estimator to train
        :type estimator: BaseEstimator
        :param dataset: the dataset to train with
        :type dataset: Dataset
        :return: the generated container if successfully trained
        :rtype: EstimatorContainer
        """
        estimator.fit(dataset.X)
        return EstimatorContainer(estimator=estimator, dataset=dataset)
