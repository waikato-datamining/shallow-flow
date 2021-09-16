# shallowflow-redis
[Redis](https://github.com/andymccurdy/redis-py) components for shallowflow.

## Actors

* Standalones

  * `shallowflow.redis.standalones.RedisConnection`

* Sources

  * `shallowflow.redis.sources.RedisSource` - allows selection of action to perform

* Transformers

  * `shallowflow.redis.transformers.RedisTransformer` - allows selection of action to perform
    
* Sinks

  * `shallowflow.redis.sinks.RedisSink` - allows selection of action to perform
  
## Examples

  * [send and receive](examples/redis_send_and_receive.py)
  * [transform data](examples/redis_transform_data.py)
