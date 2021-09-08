import os
import numpy as np
from shallowflow.api.config import AbstractOptionHandler, optionhandler_to_dict, dict_to_optionhandler
from shallowflow.api.serialization.objects import add_dict_writer, add_dict_reader


def split_off_class(data, class_index):
    """
    Splits off the class attribute from the data matrix.
    The class index can either be a 0-based int or a 1-based string
    (first,second,last,last-1 are accepted as well).
    :param data: the 2D matrix to process
    :type data: ndarray
    :param class_index: the position of the class attribute to split off
    :type class_index: int or str
    :return: the input variables (2D matrix) and the output variable (1D)
    """

    if len(data) == 0:
        num_atts = -1
    else:
        num_atts = len(data[0])

    # interpret class index
    if isinstance(class_index, str):
        if class_index == "first":
            index = 0
        elif class_index == "second":
            index = 1
        elif class_index == "last-1":
            if num_atts == -1:
                raise Exception("No data, cannot determine # of attributes for class index: %s" % class_index)
            index = num_atts - 2
        elif class_index == "last":
            if num_atts == -1:
                raise Exception("No data, cannot determine # of attributes for class index: %s" % class_index)
            index = num_atts - 1
        else:
            try:
                index = int(class_index) - 1
            except:
                raise Exception("Unsupported class index: %s" % class_index)
    elif isinstance(class_index, int):
        index = class_index
    else:
        raise Exception("Unsupported type for class index: " + str(type(class_index)))

    if index == 0:
        X = [list(r)[1:] for r in data]
    elif index == (num_atts - 1):
        X = [list(r)[0:index] for r in data]
    else:
        X = []
        for r in data:
            r = list(r)
            rn = []
            rn.extend(r[0:index])
            rn.extend(r[index+1:])
            X.append(rn)
    y = [r[index] for r in data]
    return np.array(X), np.array(y)


class AbstractDatasetLoader(AbstractOptionHandler):
    """
    Ancestor for dataset loaders.
    """

    def _check(self, path):
        """
        Check method before attempting to load the dataset.

        :param path: the path for the dataset
        :type path: str
        :return: None if successful, otherwise error message
        :rtype: str
        """
        if not os.path.exists(path):
            return "Dataset path does not exist: %s" % path
        if os.path.isdir(path):
            return "Dataset path points to directory: %s" % path
        return None

    def generates(self):
        """
        Returns the container class that the loader generates.

        :return: the container class
        """
        raise NotImplemented()

    def _do_load(self, path):
        """
        Loads the dataset.

        :param path: the path of the dataset to load
        :type path: str
        :return: the dataset
        """
        raise NotImplemented()

    def load(self, path):
        """
        Loads the specified dataset.

        :param path: the path of the dataset to load
        :type path: str
        :return: the dataset
        """
        msg = self._check(path)
        if msg is not None:
            raise Exception(msg)
        return self._do_load(path)


# register reader/writer
add_dict_writer(AbstractDatasetLoader, optionhandler_to_dict)
add_dict_reader(AbstractDatasetLoader, dict_to_optionhandler)
