import argparse
import traceback

from shallowflow.api.control import MutableActorHandler, ActorHandlerInfo
from shallowflow.api.io import load_actor, get_reader_extensions, save_actor
from shallowflow.api.scope import ScopeHandler
from shallowflow.api.storage import StorageHandler, Storage
from shallowflow.api.vars import Variables
from shallowflow.base.directors import SequentialDirector


class Flow(MutableActorHandler, StorageHandler, ScopeHandler):
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
        self._callable_names = set()

    def _new_director(self):
        """
        Returns the director to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        return SequentialDirector(owner=self, allows_standalones=True, requires_source=True, requires_sink=False)

    @property
    def actor_handler_info(self):
        """
        Returns meta-info about itself.

        :return: the info
        :rtype: ActorHandlerInfo
        """
        return ActorHandlerInfo(can_contain_standalones=True, can_contain_source=True)

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

    def is_callable_name_used(self, handler, actor):
        """
        Returns whether a callable name is already in use.

        :param handler: the handler for the actor to check
        :type handler: ActorHandler
        :param actor: the actor to check the name for
        :type actor: Actor
        :return: True if already in use
        :rtype: bool
        """
        return actor.name in self._callable_names

    def add_callable_name(self, handler, actor):
        """
        Adds the callable name, if possible.

        :param handler: the handler for the actor to add
        :type handler: ActorHandler
        :param actor: the actor to add
        :type actor: Actor
        :return: None if successfully added, otherwise error message
        :rtype: str
        """
        if self.is_callable_name_used(handler, actor):
            return "Callable name '%s' is already in use this scope (%s)!" % (actor.name, handler.parent.full_name)
        self._callable_names.add(actor.name)
        return None


def run_flow(flow, variables=None, dump_file=None):
    """
    Executes the supplied flow.

    :param flow: the actor to execute
    :type flow: Actor
    :param variables: additional variables to set
    :type variables: Variables
    :param dump_file: the file to store the flow in, e.g., for analysis
    :type dump_file: str
    :return: None if successful, otherwise error message
    :rtype: str
    """
    if dump_file is not None:
        print("Saving flow to: %s" % dump_file)
        msg = save_actor(flow, dump_file)
        if msg is not None:
            print(msg)

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
    parser.add_argument("-v", "--variable", metavar="KEY=VALUE", nargs='+', default=None, help="For supplying variables to the flow.")
    parsed = parser.parse_args(args=args)

    # any variables?
    variables = None
    if parsed.variable is not None:
        variables = Variables()
        for pair in parsed.variable:
            parts = pair.split("=")
            if len(parts) == 2:
                variables.set(parts[0].strip(), parts[1].strip())
            else:
                print("Invalid key=value pair: %s" % pair)

    flow = load_actor(parsed.flow)
    run_flow(flow, variables=variables)


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
