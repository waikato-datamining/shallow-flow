import numpy as np
from scipy.io.arff import loadarff
from shallowflow.api.config import Option
from shallowflow.sklearn.datasets import Dataset, SupervisedDataset
from ._AbstractDatasetLoader import AbstractDatasetLoader, split_off_class


class ArffLoader(AbstractDatasetLoader):
    """
    Loads ARFF files.
    """

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("class_index", str, "", "The 1-based index for the class ('first', 'second', 'last-1', 'last' are accepted as well); leave empty for no class"))

    def generates(self):
        """
        Returns the container class that the loader generates.

        :return: the container class
        """
        if len(self.get("class_index")) == 0:
            return Dataset
        else:
            return SupervisedDataset

    def _do_load(self, path):
        """
        Loads the dataset.

        :param path: the path of the dataset to load
        :type path: str
        :return: the dataset
        """
        data, meta = loadarff(path)
        if len(self.get("class_index")) == 0:
            return Dataset(np.array(data), meta=meta)
        else:
            X, y = split_off_class(data, self.get("class_index"))
            return SupervisedDataset(X, y, meta=meta)
