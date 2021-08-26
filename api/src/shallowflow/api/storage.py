STORAGE_EVENT_ADDED = "added"
STORAGE_EVENT_UPDATED = "updated"
STORAGE_EVENT_DELETED = "deleted"
STORAGE_EVENT_CLEARED = "cleared"

STORAGE_EVENTS = [
    STORAGE_EVENT_ADDED,
    STORAGE_EVENT_UPDATED,
    STORAGE_EVENT_DELETED,
    STORAGE_EVENT_CLEARED,
]

VALID_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"


def is_valid_name(s):
    """
    Checks whether the string is a valid storage name.

    :param s: the string to check
    :type s: str
    :return: True if valid
    :rtype: bool
    """
    for i in range(len(s)):
        if s[i] not in VALID_CHARS:
            return False
    return True


class StorageChangeEvent(object):
    """
    Event that gets sent out if storage changes.
    """

    def __init__(self, storage, event_type, key=None):
        """
        Initializes the event.

        :param storage: the affected storage
        :type storage: Storage
        :param event_type: the event type
        :type event_type: str
        :param key: the affected key
        :type key: str
        """
        if (event_type is not None) and (event_type not in STORAGE_EVENTS):
            raise Exception("Invalid storage event type: %s" % event_type)
        self.storage = storage
        self.event_type = event_type
        self.key = key


class StorageChangeListener(object):
    """
    Interface for classes that listen to storage change events.
    """

    def storage_changed(self, event):
        """
        Gets called when the storage changes.

        :param event: the event
        :type event: StorageChangeEvent
        """
        raise NotImplemented()


class Storage(object):
    """
    Manages the storage.
    """

    def __init__(self):
        """
        Initializes the storage.
        """
        self._data = dict()
        self._listeners = set()

    def add_listener(self, l):
        """
        Adds the listener for events.

        :param l: the listener to add
        :type l: StorageChangeListener
        """
        self._listeners.add(l)

    def remove_listener(self, l):
        """
        Removes the specified listener.

        :param l: the listener to remove
        :type l: StorageChangeListener
        """
        self._listeners.remove(l)

    def clear_listeners(self):
        """
        Removes all listeners.
        """
        self._listeners.clear()

    def clear(self):
        """
        Removes all stored items.
        """
        self._data.clear()
        self._notify_listeners(StorageChangeEvent(self, STORAGE_EVENT_CLEARED))

    def has(self, key):
        """
        Checks whether a storage item is available for the name.

        :param key: the storage name to look up
        :type key: str
        :return: True if available
        :rtype: bool
        """
        if not is_valid_name(key):
            raise Exception("Invalid storage name: %s" + key)
        return key in self._data

    def set(self, key, value):
        """
        Adds the specified storage item.

        :param key: the key for the item
        :type key: str
        :param value: the value to store
        :type value: object
        """
        if not is_valid_name(key):
            raise Exception("Invalid storage name: %s" + key)
        if key not in self._data:
            self._data[key] = value
            self._notify_listeners(StorageChangeEvent(self, STORAGE_EVENT_ADDED, key))
        else:
            self._data[key] = value
            self._notify_listeners(StorageChangeEvent(self, STORAGE_EVENT_UPDATED, key))

    def get(self, key):
        """
        Returns the storage value.

        :param key: the key to get the value for
        :type key: str
        :return: the storage value, None if not available
        :rtype: object
        """
        if not is_valid_name(key):
            raise Exception("Invalid storage name: %s" + key)
        if key in self._data:
            return self._data[key]
        else:
            return None

    def remove(self, key):
        """
        Removes the storage value.

        :param key: the name of the value to remove
        :type key: str
        """
        if not is_valid_name(key):
            raise Exception("Invalid storage name: %s" + key)
        if key in self._data:
            del self._data[key]
            self._notify_listeners(StorageChangeEvent(self, STORAGE_EVENT_DELETED, key))

    def keys(self):
        """
        Returns all the names of the currently stored items.

        :return: the set of names
        :rtype: set
        """
        return self._data.keys()

    def _notify_listeners(self, event):
        """
        Notifies all listeners with the event.

        :param event: the event to send
        :type event: StorageChangeEvent
        """
        for l in self._listeners:
            l.variables_changed(event)

    def __str__(self):
        """
        Returns a string representation of the stored items.

        :return: the stored items
        :rtype: str
        """
        return str(self._data)


class StorageHandler(object):
    """
    Interface for classes that manage storage.
    """

    @property
    def storage(self):
        """
        Returns the storage.

        :return: the storage
        :rtype: Storage
        """
        raise NotImplemented()
