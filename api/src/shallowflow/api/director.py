from .logging import LoggableObject
from shallowflow.api.actor import InputConsumer, OutputProducer, is_source, is_sink


class AbstractDirector(LoggableObject):
    """
    Ancestor for directors.
    """

    def _check(self, actors):
        """
        For performing checks.

        :param actors: the actors to execute
        :type actors: list
        :return: None if check successful, otherwise error message
        :rtype: str
        """
        if len(actors) == 0:
            return "No actors to execute!"
        return None

    def _do_execute(self, actors):
        """
        Executes the specified list of actors.

        :param actors: the actors to execute
        :type actors: list
        :return: None if successfully executed, otherwise error message
        :rtype: str
        """
        raise NotImplemented()

    def execute(self, actors):
        """
        Executes the specified list of actors.

        :param actors: the actors to execute
        :type actors: list
        :return: None if successfully executed, otherwise error message
        :rtype: str
        """
        result = self._check(actors)
        if result is None:
            result = self._do_execute(actors)
        return result


class SequentialDirector(AbstractDirector):
    """
    Executes a list of actors as a sequence (output of one is the input for the next).
    """

    def __init__(self, requires_source, requires_sink):
        """
        Initializes the director.

        :param requires_source: whether a source is required
        :type requires_source: bool
        :param requires_sink: whether a sink is required
        :type requires_sink: bool
        """
        self.requires_source = requires_source
        self.requires_sink = requires_sink

    def _check(self, actors):
        """
        For performing checks.

        :param actors: the actors to execute
        :type actors: list
        :return: None if check successful, otherwise error message
        :rtype: str
        """
        result = super()._check(actors)
        if result is None:
            if self.requires_source and not is_source(actors[0]):
                result = "First actor must be a source!"
        if result is None:
            if self.requires_sink and not is_sink(actors[-1]):
                result = "Last actor must be a source!"
        if result is None:
            for i in range(len(actors) - 1):
                if isinstance(actors[i], OutputProducer) and isinstance(actors[i+1], InputConsumer):
                    continue
                if not isinstance(actors[i], OutputProducer):
                    result = "Actor #%d does not generate output!" % (i+1)
                    break
                if not isinstance(actors[i+1], InputConsumer):
                    result = "Actor #%d does not accept input!" % (i + 2)
                    break
        return result

    def _do_execute(self, actors):
        """
        Executes the specified list of actors.

        :param actors: the actors to execute
        :type actors: list
        :return: None if successfully executed, otherwise error message
        :rtype: str
        """
        result = None
        pending_actors = []
        current_index = 0
        current_output = None
        current_actor = actors[0]

        while True:
            # provide last output as input
            if (current_output is not None) and isinstance(current_actor, InputConsumer):
                current_actor.input(current_output)
                current_output = None

            # execute actor
            msg = current_actor.execute()
            if msg is not None:
                result = "Failed to execute actor #%d: %s" % (current_index+1, msg)
                break

            # any output?
            if isinstance(current_actor, OutputProducer):
                if current_actor.has_output():
                    current_output = current_actor.output()
                if current_actor.has_output():
                    pending_actors.append(current_actor)
                if current_index < len(actors) - 1:
                    current_index += 1
                    current_actor = actors[current_index]
                else:
                    # nothing left
                    if len(pending_actors) == 0:
                        break
            else:
                if len(pending_actors) > 0:
                    current_actor = pending_actors.pop()
                    current_index = actors.index(current_actor)
                    current_output = current_actor.output()
                    if current_actor.has_output():
                        pending_actors.append(current_actor)
                    if current_index < len(actors) - 1:
                        current_index += 1
                        current_actor = actors[current_index]
                    else:
                        # nothing left
                        if len(pending_actors) == 0:
                            break
                else:
                    # nothing left
                    break

        return result
