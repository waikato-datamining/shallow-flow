import os
import redis
from shallowflow.base.controls import Flow, run_flow
from shallowflow.base.sources import ForLoop
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.redis.standalones import RedisConnection
from shallowflow.redis.transformers import RedisTransformer
from shallowflow.redis.transformers.action import BroadcastAndListen

channel_in = "dummy_in"
channel_out = "dummy_out"

# dummy redis process, simply appends "-done" to incoming data
r = redis.Redis()
p = r.pubsub()
def anon_handler(message):
    d = message['data'].decode() + "-done"
    r.publish(channel_in, d)
p.psubscribe(**{channel_out: anon_handler})
p.run_in_thread(sleep_time=0.001)

# flow that pushes data through dummy redis process
flow = Flow().manage([
    RedisConnection(),
    ForLoop(),
    RedisTransformer({"action": BroadcastAndListen({"channel_out": channel_out, "channel_in": channel_in})}),
    ConsoleOutput(),
])
msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)

# all data processed, user has to manually stop dummy redis process
print("Please press Ctrl+C to stop dummy redis process...")
