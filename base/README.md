# shallow-flow-base
The core components for shallow-flow.

## Actors

* Control actors

  * shallowflow.base.controls.Flow
  * shallowflow.base.controls.Tee
  * shallowflow.base.controls.ConditionalTee

* Sources

  * shallowflow.base.sources.DirectoryLister
    
* Transformers

  * shallowflow.base.transformers.PassThrough
    
* Sinks

  * shallowflow.base.sinks.ConsoleOutput
  * shallowflow.base.sinks.Null

## Conditions

* shallowflow.base.conditions.AlwaysFalse
* shallowflow.base.conditions.AlwaysTrue
