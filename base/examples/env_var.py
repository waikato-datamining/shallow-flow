import os
from shallowflow.base.controls import Flow, run_flow
from shallowflow.base.standalones import SetVariable
from shallowflow.base.sources import GetVariable
from shallowflow.base.sinks import ConsoleOutput

flow = Flow().manage([
    SetVariable({
        "var_name": "v",
        "var_value": "value_from_flow",
        "env_var": "FLOW_VAR",
        "env_var_optional": True,   # if optional, no error gets generated when FLOW_VAR not set
    }),
    GetVariable({"var_name": "v"}),
    ConsoleOutput(),
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
