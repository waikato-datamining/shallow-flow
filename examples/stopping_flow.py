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
run_flow(flow)
