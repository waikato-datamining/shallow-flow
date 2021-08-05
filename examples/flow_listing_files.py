from os.path import expanduser
from shallowflow.base.controls import Flow
from shallowflow.base.sources import DirectoryLister
from shallowflow.base.transformers import PassThrough
from shallowflow.base.sinks import ConsoleOutput

dl = DirectoryLister()
dl.set("dir", expanduser("~"))
dl.set("list_files", True)
dl.set("list_dirs", True)
dl.set("sort", True)
dl.set("recursive", True)
dl.set("max_items", 100)

pt = PassThrough()

co = ConsoleOutput()

flow = Flow()
flow.actors = [dl, pt, co]

msg = flow.setup()
if msg is None:
    msg = flow.execute()
    if msg is not None:
        print(msg)
else:
    print(msg)
