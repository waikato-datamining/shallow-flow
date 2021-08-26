# shallow-flow-base
The core components for shallow-flow.

## Actors

* Control actors

  * `shallowflow.base.controls.Flow`
  * `shallowflow.base.controls.Tee`
  * `shallowflow.base.controls.ConditionalTee`
    
* Directors

  * `shallowflow.base.directors.SequentialDirector`

* Standalones

  * `shallowflow.base.standalones.SetVariable`

* Sources

  * `shallowflow.base.sources.DirectoryLister`
  * `shallowflow.base.sources.ForLoop`
  * `shallowflow.base.sources.GetStorage`
  * `shallowflow.base.sources.GetVariable`
    
* Transformers

  * `shallowflow.base.transformers.PassThrough`
  * `shallowflow.base.transformers.SetStorage`
  * `shallowflow.base.transformers.SetVariable`
    
* Sinks

  * `shallowflow.base.sinks.ConsoleOutput`
  * `shallowflow.base.sinks.Null`

## Conditions

* `shallowflow.base.conditions.AlwaysFalse`
* `shallowflow.base.conditions.AlwaysTrue`

## Help

  * `shallowflow.base.help.PlainText` - plain text help
