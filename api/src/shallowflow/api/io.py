import json
import traceback
import yaml
from .actor import Actor, actor_to_dict, dict_to_actor


def load_actor(path):
    """
    Loads a actor from the given file.

    :param path: the file containing an actor in JSON (.json) or YAML (.yaml) format.
    :type path: str
    :return: the actor, None if failed to load
    :rtype: Actor
    """
    try:
        if path.lower().endswith(".json"):
            with open(path, "r") as jf:
                d = json.load(jf)
            return dict_to_actor(d)
        elif path.lower().endswith(".yaml"):
            with open(path, "r") as yf:
                d = yaml.safe_load(yf)
        return dict_to_actor(d)
    except:
        print("Failed to load actor from: %s\n%s" % (path, traceback.format_exc()))
        return None


def save_actor(actor, path):
    """
    Saves the actor to the given file.

    :param actor: the actor to save
    :type actor: Actor
    :param path: the file to save the actor in JSON (.json) or YAML (.yaml) format
    :type path: str
    :return: None if successfully saved, otherwise error message
    :rtype: str
    """
    d = actor_to_dict(actor)
    try:
        if path.lower().endswith(".json"):
            with open(path, "w") as jf:
                json.dump(d, jf, indent=2)
            return None
        elif path.lower().endswith(".yaml"):
            with open(path, "w") as yf:
                yaml.safe_dump(d, yf)
        return None
    except:
        return "Failed to save actor to: %s\n%s" % (path, traceback.format_exc())
