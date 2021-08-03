from datetime import datetime


def log(*args):
    """
    Just outputs the arguments with a timestamp.

    :param args: the arguments to log
    """
    print(*("%s - " % str(datetime.now()), *args))


class LoggableObject(object):
    """
    Ancestor for objects that can output logging information.
    """

    def log(self, *args):
        """
        Logs the arguments.

        :param args: the arguments to log
        """
        print(*("%s - %s -" % (type(self).__name__, str(datetime.now())), *args))
