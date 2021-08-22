from os.path import expanduser
from shallowflow.base.controls import Flow, run_flow
from shallowflow.base.sources import DirectoryLister
from shallowflow.base.transformers import PassThrough
from shallowflow.base.sinks import ConsoleOutput

dl = DirectoryLister() \
    .set("dir", expanduser("~"))\
    .set("list_files", True)\
    .set("list_dirs", True)\
    .set("sort", True)\
    .set("recursive", True)\
    .set("max_items", 100)\
    .set("debug", True)

pt = PassThrough()

co = ConsoleOutput()

flow = Flow()
flow.actors = [dl, pt, co]

msg = run_flow(flow)
if msg is not None:
    print(msg)
