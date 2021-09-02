import os
from shallowflow.base.controls import Flow, WhileLoop, run_flow
from shallowflow.base.conditions import NumExpr
from shallowflow.base.sources import Start, GetVariable
from shallowflow.base.transformers import SetVariable, IncVariable
from shallowflow.base.sinks import ConsoleOutput

flow = Flow().manage([
    Start(),
    SetVariable(options={"var_name": "i", "var_value": "1"}),
    WhileLoop(options={"condition": NumExpr(options={"expression": "@{i} < 5"})}).manage([
        GetVariable(options={"var_name": "i"}),
        IncVariable(options={"var_name": "i"}),
        ConsoleOutput(),
    ]),
])
msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
