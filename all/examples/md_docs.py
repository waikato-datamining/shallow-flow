from shallowflow.api.help import class_hierarchy_help
from shallowflow.api.actor import Actor
from shallowflow.base.help import Markdown

# the following generates Markdown documents for all actors
# in the "output" directory
files = class_hierarchy_help(Actor, Markdown(), "./output")

# the files that got generated, relative to the output dir
print(files)
