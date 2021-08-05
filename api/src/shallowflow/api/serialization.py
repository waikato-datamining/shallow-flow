DICT_READERS = None
DICT_WRITERS = None


def get_dict_readers():
    global DICT_READERS
    if DICT_READERS is None:
        DICT_READERS = dict()
    return DICT_READERS


def add_dict_reader(cls, handler):
    get_dict_readers()[cls] = handler


def has_dict_reader(cls):
    return cls in get_dict_readers()


def get_dict_reader(cls):
    if has_dict_reader(cls):
        return get_dict_readers()[cls]
    else:
        return None


def get_dict_writers():
    global DICT_WRITERS
    if DICT_WRITERS is None:
        DICT_WRITERS = dict()
    return DICT_WRITERS


def add_dict_writer(cls, handler):
    get_dict_writers()[cls] = handler


def has_dict_writer(cls):
    return cls in get_dict_writers()


def get_dict_writer(cls):
    if has_dict_writer(cls):
        return get_dict_writers()[cls]
    else:
        return None
