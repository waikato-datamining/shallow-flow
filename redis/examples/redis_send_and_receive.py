import os
from shallowflow.base.controls import Flow, Tee, Trigger, Sleep, run_flow
from shallowflow.base.sources import ForLoop
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.redis.standalones import RedisConnection
from shallowflow.redis.sources import RedisSource
from shallowflow.redis.sources.action import Get
from shallowflow.redis.sinks import RedisSink
from shallowflow.redis.sinks.action import Set


flow = Flow().manage([
    RedisConnection(),
    ForLoop(),
    Tee().manage([
        RedisSink({"action": Set({"key": "name"})})
    ]),
    Trigger().manage([
        RedisSource({"action": Get({"key": "name"})}),
        ConsoleOutput()
    ]),
    Sleep(),
])
msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
