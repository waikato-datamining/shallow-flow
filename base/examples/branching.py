from scoping import scoping
from shallowflow.base.controls import Flow, Branch, Sequence, run_flow
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.base.sources import ForLoop
from shallowflow.base.transformers import PassThrough

forloop = ForLoop()

branch = Branch()
# generates five branches with different prefixes for the console output
for i in range(5):
    with scoping():
        seq = Sequence()
        pt = PassThrough()  # added for the sequence to make sense :-)
        output = ConsoleOutput() \
            .set("prefix", "branch-" + str(len(branch.actors) + 1) + ": ")
        seq.actors = [pt, output]
        branch.append(seq)

flow = Flow()
flow.actors = [forloop, branch]
msg = run_flow(flow)
if msg is not None:
    print(msg)
