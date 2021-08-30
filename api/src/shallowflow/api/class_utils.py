import os
from setuptools import find_namespace_packages
import inspect
import importlib
from shallowflow.api.serialization.objects import get_dict_reader


def fix_module_name(module, cls):
    """
    Turns a.b._C.C into a.b.C if possible.

    :param module: the module
    :type module: str
    :param cls: the class name
    :type cls: str
    :return: the (potentially) updated tuple of module and class name
    """
    if module.split(".")[-1].startswith("_"):
        try:
            module_short = ".".join(module.split(".")[:-1])
            getattr(importlib.import_module(module_short), cls)
            module = module_short
        except Exception:
            pass
    return module, cls


def find_module_names():
    """
    Locates all module names used by shallowflow.

    :return: the list of module names
    :rtype: list
    """
    result = []
    location = inspect.getmodule(get_dict_reader).__file__
    if "shallow-flow" in location:
        while not location.endswith("shallow-flow"):
            location = os.path.dirname(location)
    else:
        while not location.endswith("shallowflow"):
            location = os.path.dirname(location)

    packages = find_namespace_packages(where=location)

    for package in packages:
        if ".src." in package:
            module_name = package[package.index(".src.") + 5:]
        else:
            module_name = "shallowflow." + package
        try:
            module = importlib.import_module(module_name)
            if module.__package__ not in result:
                result.append(module.__package__)
        except Exception:
            pass
    result.sort()
    return result


def find_classes(super_class):
    """
    Finds all classes that are derived from the specified superclass in all of the
    shallowflow modules.

    :param super_class: the class to look for
    :type super_class: type
    :return: the list of class names
    :rtype: list
    """
    result = []
    module_names = find_module_names()

    for module_name in module_names:
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, super_class):
                    module_name, c = fix_module_name(obj.__module__, obj.__name__)
                    result.append(module_name + "." + c)
        except Exception:
            pass
    result.sort()
    return result
