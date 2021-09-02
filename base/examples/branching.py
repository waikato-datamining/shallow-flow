import os

from shallowflow.base.controls import Flow, Branch, Sequence, run_flow
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.base.sources import ForLoop
from shallowflow.base.transformers import PassThrough

branches = []
for i in range(5):
    seq = Sequence().manage([
        PassThrough(),  # added for the sequence to make sense :-)
        ConsoleOutput({"prefix": "branch-" + str(len(branches) + 1) + ": "}),
    ])
    branches.append(seq)

flow = Flow().manage([
    ForLoop(),
    Branch().manage(branches)
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
