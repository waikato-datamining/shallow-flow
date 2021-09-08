class DefaultDataset(object):
    """
    Container class for datasets.
    """

    def __init__(self, X, meta=None):
        """
        Initializes the container.

        :param X: the input variables
        :param meta: optional meta-data
        """
        self.X = X
        self.meta = meta

    def __str__(self):
        """
        Returns a simple string representation.

        :return: the string representation
        :rtype: str
        """
        return "X=" + str(self.X) + "\nmeta=" + str(self.meta)


class ClassificationDataset(DefaultDataset):
    """
    Container class for classification datasets.
    """

    def __init__(self, X, y, meta=None):
        """
        Initializes the container.

        :param X: the input variables
        :param y: the output variable(s)
        :param meta: optional meta-data
        """
        super().__init__(X, meta)
        self.y = y

    def __str__(self):
        """
        Returns a simple string representation.

        :return: the string representation
        :rtype: str
        """
        return "X=" + str(self.X) + "\ny=" + str(self.y) + "\nmeta=" + str(self.meta)
