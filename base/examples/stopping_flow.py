import os
from shallowflow.base.controls import Flow, Stop, ConditionalTee, run_flow
from shallowflow.base.conditions import NumExpr
from shallowflow.base.sources import ForLoop
from shallowflow.base.transformers import SetVariable
from shallowflow.base.sinks import ConsoleOutput

loop = ForLoop()

setvar = SetVariable(options={"var_name": "i"})

numexpr = NumExpr(options={"expression": "@{i} > 5"})
tee = ConditionalTee(options={"condition": numexpr, "actors": [Stop()]})

output = ConsoleOutput()

flow = Flow()
flow.actors = [loop, setvar, tee, output]
msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
