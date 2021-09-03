import os
from shallowflow.api.callable import CallableActorReference
from shallowflow.base.controls import Flow, run_flow
from shallowflow.base.standalones import CallableActors
from shallowflow.base.sources import ForLoop, CallableSource
from shallowflow.base.transformers import CallableTransformer, PassThrough
from shallowflow.base.sinks import ConsoleOutput, CallableSink

flow = Flow().manage([
    CallableActors().manage([
        ForLoop({"name": "fl"}),
        PassThrough({"name": "pt"}),
        ConsoleOutput({"name": "co"}),
    ]),
    CallableSource({"callable_name": CallableActorReference("fl")}),
    CallableTransformer({"callable_name": CallableActorReference("pt")}),
    CallableSink({"callable_name": CallableActorReference("co")}),
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
