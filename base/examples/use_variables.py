import os

from shallowflow.base.conditions import NumExpr
from shallowflow.base.controls import Flow, ConditionalTrigger, run_flow
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.base.sources import ForLoop
from shallowflow.base.transformers import SetVariable

output1 = ConsoleOutput({"prefix": "all: "})

flow = Flow().manage([
    ForLoop({"start": 1, "end": 5}),
    SetVariable({"var_name": "upper", "debug": False}),
    ConditionalTrigger({"condition": NumExpr({"expression": "@{upper} > 3"})}).manage([
        ForLoop({"end": "@{upper}"}),
        ConsoleOutput({"prefix": "conditional: "}),
    ]),
    ConsoleOutput({"prefix": "all: "}),
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
