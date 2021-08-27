from scoping import scoping
from shallowflow.base.controls import Flow, WhileLoop, run_flow
from shallowflow.base.conditions import NumExpr
from shallowflow.base.sources import Start, ForLoop, GetVariable
from shallowflow.base.transformers import SetVariable, IncVariable
from shallowflow.base.sinks import ConsoleOutput

start = Start()

# initialize variable
setvar = SetVariable() \
    .set("var_name", "i") \
    .set("var_value", "1")

# only execute while loop as lo
numexpr = NumExpr() \
    .set("expression", "@{i} < 5")
while_loop = WhileLoop() \
    .set("condition", numexpr)
with scoping():
    getvar = GetVariable() \
        .set("var_name", "i")

    incvar = IncVariable() \
        .set("var_name", "i")

    output = ConsoleOutput()

    while_loop.actors = [getvar, incvar, output]

flow = Flow()
flow.actors = [start, setvar, while_loop]
run_flow(flow)
