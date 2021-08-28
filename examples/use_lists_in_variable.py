from scoping import scoping
from os.path import expanduser
from shallowflow.base.controls import Flow, Trigger, run_flow
from shallowflow.base.sources import DirectoryLister, FileSupplier
from shallowflow.base.transformers import SetVariable
from shallowflow.base.sinks import ConsoleOutput

dl = DirectoryLister(options={
    "dir": expanduser("~"),
    "list_files": True,
    "list_dirs": True,
    "sort": True,
    "recursive": True,
    "max_items": 100,
    "output_as_list": True,
})
setvar = SetVariable(options={"var_name": "files"})
trigger = Trigger()
with scoping():
    lister = FileSupplier(options={"files": "@{files}"})
    output = ConsoleOutput()
    trigger.actors = [lister, output]

flow = Flow()
flow.actors = [dl, setvar, trigger]
run_flow(flow)
