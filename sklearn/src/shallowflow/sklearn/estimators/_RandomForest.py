from shallowflow.api.config import Option
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from ._AbstractEstimatorConfiguration import AbstractEstimatorConfiguration


class AbstractRandomForestConfiguration(AbstractEstimatorConfiguration):
    """
    Ancestor for a RandomForest estimators.
    """

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("n_estimators", int, 100, "The number of trees in the forest."))
        # TODO

    def _check(self):
        """
        Hook method before configuring the estimator.

        :return: None if successful check, otherwise error message
        :rtype: str
        """
        result = super()._check()
        # TODO
        return result


class RandomForestClassifierConfiguration(AbstractRandomForestConfiguration):
    """
    Configures a RandomForest classifier.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Simply loads an estimator from a pickled file."

    def _do_configure(self):
        """
        Performs the actual configuring of the estimator.

        :return: the estimator
        :rtype: BaseEstimator
        """
        return RandomForestClassifier(
            n_estimators=self.get("n_estimators")
            # TODO
        )


class RandomForestRegressorConfiguration(AbstractRandomForestConfiguration):
    """
    Configures a RandomForest regressor.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Simply loads an estimator from a pickled file."

    def _do_configure(self):
        """
        Performs the actual configuring of the estimator.

        :return: the estimator
        :rtype: BaseEstimator
        """
        return RandomForestRegressor(
            n_estimators=self.get("n_estimators")
            # TODO
        )
