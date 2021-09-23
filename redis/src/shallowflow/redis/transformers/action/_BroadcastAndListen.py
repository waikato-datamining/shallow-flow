from datetime import datetime
from time import sleep
from ._AbstractAction import AbstractAction
from shallowflow.api.compatibility import Unknown
from shallowflow.api.config import Option


class BroadcastAndListen(AbstractAction):
    """
    Broadcasts the incoming data to the specified out channel and listens for data to come through on the in channel.
    """

    def description(self):
        """
        Returns a description for the object.

        :return: the object description
        :rtype: str
        """
        return "Broadcasts the incoming data to the specified out channel and listens for data to come through on the in channel."

    def _define_options(self):
        """
        For configuring the options.
        """
        super()._define_options()
        self._option_manager.add(Option("out_as_string", bool, False, "If enabled, outgoing data get treated as string"))
        self._option_manager.add(Option("channel_out", str, "", "The channel to send the data to"))
        self._option_manager.add(Option("in_as_string", bool, False, "If enabled, incoming data get treated as string"))
        self._option_manager.add(Option("channel_in", str, "", "The channel to listen for incoming data"))
        self._option_manager.add(Option("timeout", float, 0.0, "The timeout in seconds for data to appear on the incoming channel; use <=0 for no timeout"))

    def accepts(self):
        """
        Returns the types that are accepted.

        :return: the list of types
        :rtype: list
        """
        return [Unknown]

    def generates(self):
        """
        Returns the types that get generated.

        :return: the list of types
        :rtype: list
        """
        return [Unknown]

    def _do_execute(self, connection, o):
        """
        Executes the action using the specified connection and forwards the object.

        :param connection: the Redis connection to use
        :type connection: redis.Redis
        :param o: the object to use
        :return: the retrieved object, None if not available
        """
        out_as_string = self.get("out_as_string")
        in_as_string = self.get("in_as_string")
        self._pubsub = connection.pubsub()
        self._output = None
        actor = self

        def anon_handler(message):
            data = message['data']
            if in_as_string:
                data = data.decode()
            actor._output = data
            actor._pubsub_thread.stop()
            actor._pubsub.close()
            actor._pubsub = None

        self._pubsub.psubscribe(**{self.get("channel_in"): anon_handler})
        self._pubsub_thread = self._pubsub.run_in_thread(sleep_time=0.001)

        if out_as_string:
            o = str(o)
        connection.publish(self.get("channel_out"), o)

        # wait for data to show up
        timeout = self.get("timeout")
        start = datetime.now()
        no_data = False
        while (self._pubsub is not None) and not self.is_stopped:
            sleep(0.01)
            if timeout > 0:
                end = datetime.now()
                if (end - start).total_seconds() >= timeout:
                    self.log("Timeout reached!")
                    no_data = True
                    break

        if self.is_stopped or no_data:
            if self._pubsub is not None:
                self._pubsub_thread.stop()
                self._pubsub.close()
                self._pubsub = None
            return None
        else:
            return self._output
