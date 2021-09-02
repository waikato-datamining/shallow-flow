import os
from os.path import expanduser
from shallowflow.base.controls import Flow, run_flow
from shallowflow.base.sources import DirectoryLister
from shallowflow.base.transformers import PassThrough
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.api.io import Directory

flow = Flow().manage([
    DirectoryLister({
        "dir": Directory(expanduser("~")),
        "list_files": True,
        "list_dirs": True,
        "sort": True,
        "recursive": True,
        "max_items": 100,
        "debug": True}),
    PassThrough(),
    ConsoleOutput(),
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
