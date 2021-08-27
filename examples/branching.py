from scoping import scoping
from shallowflow.base.controls import Flow, Branch, run_flow
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.base.sources import ForLoop

forloop = ForLoop()

branch = Branch()
# generates five branches with different prefixes for the console output
for i in range(5):
    with scoping():
        output = ConsoleOutput() \
            .set("prefix", "branch-" + str(len(branch.actors) + 1) + ": ")
        branch.append(output)

flow = Flow()
flow.actors = [forloop, branch]
run_flow(flow)
