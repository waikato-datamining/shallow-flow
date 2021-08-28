from scoping import scoping
from shallowflow.base.controls import Flow, WhileLoop, run_flow
from shallowflow.base.conditions import NumExpr
from shallowflow.base.sources import Start, GetVariable
from shallowflow.base.transformers import SetVariable, IncVariable
from shallowflow.base.sinks import ConsoleOutput

start = Start()

# initialize variable
setvar = SetVariable(options={"var_name": "i", "var_value": "1"})

# only execute while loop as lo
numexpr = NumExpr(options={"expression": "@{i} < 5"})
while_loop = WhileLoop(options={"condition": numexpr})
with scoping():
    getvar = GetVariable(options={"var_name": "i"})

    incvar = IncVariable(options={"var_name": "i"})

    output = ConsoleOutput()

    while_loop.actors = [getvar, incvar, output]

flow = Flow()
flow.actors = [start, setvar, while_loop]
run_flow(flow)
