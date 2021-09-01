from shallowflow.api.class_utils import find_module_names, find_classes
from shallowflow.api.actor import Actor
from shallowflow.api.config import AbstractOptionHandler

# lists all the shallowflow-related modules
print("\n--> Module names\n")
module_names = find_module_names()
for module_name in module_names:
    print(module_name)

# lists all the available shallowflow actors in the installation
print("\n--> Actors\n")
classes = find_classes(Actor)
for cls in classes:
    print(cls)

# lists all the available shallowflow optionhandler classes in the installation
print("\n--> OptionHandler\n")
classes = find_classes(AbstractOptionHandler)
for cls in classes:
    print(cls)
