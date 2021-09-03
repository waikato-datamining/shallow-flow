import os
from shallowflow.base.controls import Flow, run_flow
from shallowflow.redis.standalones import RedisConnection
from shallowflow.base.sources import ForLoop

flow = Flow().manage([
    RedisConnection(),
    ForLoop(),
    # TODO redis sink
])
msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
