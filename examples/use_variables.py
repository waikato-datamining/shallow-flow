from scoping import scoping
from shallowflow.base.controls import Flow, ConditionalTrigger, run_flow
from shallowflow.base.conditions import NumExpr
from shallowflow.base.sources import ForLoop
from shallowflow.base.transformers import SetVariable
from shallowflow.base.sinks import ConsoleOutput

loop1 = ForLoop() \
    .set("start", 1) \
    .set("end", 5)

setvar1 = SetVariable() \
    .set("var_name", "upper") \
    .set("debug", False)

# use variable in the expression itself
# only when @{upper} is greater than 3 will the sub-flow get executed
numexpr = NumExpr() \
    .set("expression", "@{upper} > 3")
trigger1 = ConditionalTrigger() \
    .set("condition", numexpr)

with scoping():
    loop2 = ForLoop()
    # attached variable @{upper} to the "end" property
    loop2.option_manager.set_var("end", "upper")
    loop2.set("debug", False)

    output2 = ConsoleOutput() \
        .set("prefix", "conditional: ")

    trigger1.actors = [loop2, output2]

output1 = ConsoleOutput() \
    .set("prefix", "all: ")

flow = Flow()
flow.actors = [loop1, setvar1, trigger1, output1]
run_flow(flow)
