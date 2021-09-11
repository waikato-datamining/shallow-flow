from shallowflow.api.transformer import AbstractSimpleTransformer
from shallowflow.api.config import Option
from shallowflow.api.io import File
from shallowflow.sklearn.transformers.datasetloaders import AbstractDatasetLoader, ArffLoader


class DatasetLoader(AbstractSimpleTransformer):
    """
    Dummy, just passes through the data.
    """

    def description(self):
        """
        Returns a description for the actor.

        :return: the actor description
        :rtype: str
        """
        return "Dummy, just passes through the data."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("loader", AbstractDatasetLoader, ArffLoader(), "Loads the dataset from the incoming file"))

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [File]

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [self.get("loader").generates()]

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        result = None
        loader = self.get("loader")

        try:
            dataset = loader.load(self._input)
            self._output.append(dataset)
        except:
            result = self._handle_exception("Failed to load dataset: %s" % self._input)

        return result
