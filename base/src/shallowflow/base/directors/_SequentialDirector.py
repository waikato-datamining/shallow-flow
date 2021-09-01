from shallowflow.api.director import AbstractDirector
from shallowflow.api.actor import InputConsumer, OutputProducer, is_source, is_sink, is_standalone


class SequentialDirector(AbstractDirector):
    """
    Executes a list of actors as a sequence (output of one is the input for the next).
    """

    def __init__(self, owner, allows_standalones, requires_source, requires_sink):
        """
        Initializes the director.

        :param allows_standalones: whether standalones are allowed
        :type allows_standalones: bool
        :param requires_source: whether a source is required
        :type requires_source: bool
        :param requires_sink: whether a sink is required
        :type requires_sink: bool
        """
        super().__init__(owner)
        self.allows_standalones = allows_standalones
        self.requires_source = requires_source
        self.requires_sink = requires_sink
        self._actors = None

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
            if self.requires_source:
                for i in range(len(actors)):
                    if is_standalone(actors[i]):
                        continue
                    if is_source(actors[i]):
                        break
                    else:
                        result = "First (non-standalone) actor must be a source!"

        if result is None:
            if self.requires_sink and not is_sink(actors[-1]):
                result = "Last actor must be a sink!"

        if result is None:
            for i in range(len(actors) - 1):
                if is_standalone(actors[i]):
                    continue
                if isinstance(actors[i], OutputProducer) and isinstance(actors[i+1], InputConsumer):
                    continue
                if not isinstance(actors[i], OutputProducer):
                    result = "Actor #%d does not generate output!" % (i+1)
                    break
                if not isinstance(actors[i+1], InputConsumer):
                    result = "Actor #%d does not accept input!" % (i + 2)
                    break

        return result

    def _execute_standalones(self, actors):
        """
        Executes all the standalones and returns the index of the
        :param actors:
        :return:
        """
        result = 0

        if not self.allows_standalones:
            return result

        for i in range(len(actors)):
            if is_standalone(actors[i]):
                result = i
                msg = actors[i].execute()
                if msg is not None:
                    raise Exception(msg)
            else:
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
        start_index = self._execute_standalones(actors)
        not_finished_actor = actors[start_index]
        pending_actors = []
        finished = False

        while not self.is_stopped and not finished:
            # determine starting point
            if len(pending_actors) > 0:
                start_index = actors.index(pending_actors[-1])
            else:
                start_index = actors.index(not_finished_actor)
                not_finished_actor = None

            # iterate over actors
            token = None
            curr = None
            for i in range(start_index, len(actors), 1):
                curr = actors[i]
                if token is None:
                    if isinstance(curr, OutputProducer) and curr.has_output():
                        if len(pending_actors) > 0:
                            pending_actors.pop()
                    else:
                        actor_result = curr.execute()
                        if actor_result is not None:
                            self.log(actor_result)
                            result = actor_result
                            not_finished_actor = None
                            if curr.get("stop_flow_on_error"):
                                break

                    if isinstance(curr, OutputProducer) and curr.has_output():
                        token = curr.output()
                    else:
                        token = None

                    # more to come?
                    if isinstance(curr, OutputProducer) and curr.has_output():
                        pending_actors.append(curr)

                else:
                    curr.input(token)
                    actor_result = curr.execute()
                    if actor_result is not None:
                        self.log(actor_result)
                        result = actor_result
                        not_finished_actor = None
                        if curr.get("stop_flow_on_error"):
                            break

                    # token produced?
                    if isinstance(curr, OutputProducer):
                        if curr.has_output():
                            token = curr.output()
                        else:
                            token = None

                        if curr.has_output():
                            pending_actors.append(curr)
                    else:
                        token = None

                if isinstance(curr, OutputProducer) and (token is None):
                    break

            finished = (not_finished_actor is None) and (len(pending_actors) == 0)

        return result

    def stop_execution(self):
        """
        Stops the actor execution.
        """
        if self._actors is not None:
            for actor in self._actors:
                actor.stop_execution()
        super().stop_execution()
