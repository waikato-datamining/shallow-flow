import os
from shallowflow.base.controls import Flow, Stop, ConditionalTee, run_flow
from shallowflow.base.conditions import NumExpr
from shallowflow.base.sources import ForLoop
from shallowflow.base.transformers import SetVariable
from shallowflow.base.sinks import ConsoleOutput

flow = Flow().manage([
    ForLoop(),
    SetVariable({"var_name": "i"}),
    ConditionalTee({"condition": NumExpr({"expression": "@{i} > 5"})}).manage([
        Stop(),
    ]),
    ConsoleOutput(),
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
