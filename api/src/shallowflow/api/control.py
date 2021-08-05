from .actor import Actor
from .config import Option


class ActorHandler(Actor):
    """
    Interface for actors that manage sub-actors.
    """

    def initialize(self):
        """
        Performs initializations.
        """
        super(ActorHandler, self).initialize()
        self.option_manager.add(Option(name="actors", value_type=list, def_value=list(),
                                       help="The sub-actors to manage", base_type=Actor))

    def _director(self):
        """
        Returns the directory to use for executing the actors.

        :return: the director
        :rtype: AbstractDirector
        """
        raise NotImplemented()

    @property
    def actors(self):
        """
        Returns the current sub-actors.

        :return: the sub-actors
        :rtype: list
        """
        return self._option_manager.get("actors")

    @actors.setter
    def actors(self, actors):
        """
        Sets the new sub-actors.

        :param actors: the new actors
        :type actors: list
        """
        for a in actors:
            if not isinstance(a, Actor):
                raise Exception("Can only set objects of type Actor!")
            a.parent = self

        # ensure that names are unique
        names = []
        for a in actors:
            name = a.name
            if name in names:
                i = 1
                while name in names:
                    i += 1
                    name = a.name + " (" + str(i) + ")"
                a.set("name", name)
                names.append(name)
            else:
               names.append(name)

        self._option_manager.set("actors", actors)

    def _do_execute(self):
        """
        Performs the actual execution.

        :return: None if successful, otherwise error message
        :rtype: str
        """
        return self._director().execute(self.actors)
