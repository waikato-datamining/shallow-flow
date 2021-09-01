import os
from scoping import scoping
from shallowflow.base.controls import Flow, ConditionalTrigger, run_flow
from shallowflow.base.conditions import NumExpr
from shallowflow.base.sources import ForLoop
from shallowflow.base.transformers import SetVariable
from shallowflow.base.sinks import ConsoleOutput

loop1 = ForLoop(options={"start": 1, "end": 5})

setvar1 = SetVariable(options={"var_name": "upper", "debug": False})

# use variable in the expression itself
# only when @{upper} is greater than 3 will the sub-flow get executed
numexpr = NumExpr(options={"expression": "@{upper} > 3"})
trigger1 = ConditionalTrigger(options={"condition": numexpr})

with scoping():
    # attached variable @{upper} to the "end" property
    loop2 = ForLoop(options={"end": "@{upper}"})

    output2 = ConsoleOutput(options={"prefix": "conditional: "})

    trigger1.actors = [loop2, output2]

output1 = ConsoleOutput(options={"prefix": "all: "})

flow = Flow()
flow.actors = [loop1, setvar1, trigger1, output1]
msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
