import argparse
import traceback

from shallowflow.api.control import MutableActorHandler
from shallowflow.api.io import load_actor, get_reader_extensions
from shallowflow.api.storage import StorageHandler, Storage
from shallowflow.api.vars import Variables
from shallowflow.base.directors import SequentialDirector


class Flow(MutableActorHandler, StorageHandler):
    """
    Encapsulates a complete flow.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Encapsulates a complete flow."

    def _initialize(self):
        """
        Initializes the members.
        """
        super()._initialize()
        self._storage = Storage()

    def _new_director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, allows_standalones=True, requires_source=True, requires_sink=False)

    def _pre_execute(self):
        """
        Before the actual code gets executed.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        # push down Variables instance
        result = super()._pre_execute()
        if result is None:
            self.update_variables(self.variables)
        return result

    @property
    def storage(self):
        """
        Returns the storage.

        :return: the storage
        :rtype: Storage
        """
        return self._storage


def run_flow(flow, variables=None):
    """
    Executes the supplied flow.

    :param flow: the actor to execute
    :type flow: Actor
    :param variables: additional variables to set
    :type variables: Variables
    :return: None if successful, otherwise error message
    :rtype: str
    """
    msg = flow.setup()
    if msg is None:
        if variables is not None:
            flow.variables.merge(variables)
        msg = flow.execute()
        if msg is not None:
            return "Failed to execute flow: %s" % msg
    else:
        return "Failed to setup flow: %s" % msg
    flow.wrap_up()
    flow.clean_up()


def main(args=None):
    """
    The main method for parsing command-line arguments and labeling.

    :param args: the commandline arguments, uses sys.argv if not supplied
    :type args: list
    """
    parser = argparse.ArgumentParser(
        description="Executes the specified flow.",
        prog="sf-runflow",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--flow", metavar="FILE", help="the flow to execute, supported extensions: " + ", ".join(get_reader_extensions()), required=True)
    parsed = parser.parse_args(args=args)
    flow = load_actor(parsed.flow)
    run_flow(flow)


def sys_main() -> int:
    """
    Runs the main function using the system cli arguments, and
    returns a system error code.

    :return: 0 for success, 1 for failure.
    """
    try:
        main()
        return 0
    except Exception:
        print(traceback.format_exc())
        return 1


if __name__ == '__main__':
    main()
