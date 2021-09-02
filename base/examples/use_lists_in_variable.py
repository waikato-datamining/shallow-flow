import os
from scoping import scoping
from os.path import expanduser
from shallowflow.base.controls import Flow, Trigger, run_flow
from shallowflow.base.sources import DirectoryLister, FileSupplier
from shallowflow.base.transformers import SetVariable
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
        "output_as_list": True,
    }),
    SetVariable({"var_name": "files"}),
    Trigger().manage([
        FileSupplier({"files": "@{files}"}),
        ConsoleOutput(),
    ]),
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
