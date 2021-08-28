# shallow-flow-base
The base components for shallow-flow.

## Actors

* Control actors

  * `shallowflow.base.controls.Branch`
  * `shallowflow.base.controls.ConditionalTee`
  * `shallowflow.base.controls.ConditionalTrigger`
  * `shallowflow.base.controls.Flow`
  * `shallowflow.base.controls.Sequence`
  * `shallowflow.base.controls.Sleep`
  * `shallowflow.base.controls.Stop`
  * `shallowflow.base.controls.Tee`
  * `shallowflow.base.controls.Trigger`
  * `shallowflow.base.controls.WhileLoop`
    
* Directors

  * `shallowflow.base.directors.SequentialDirector`

* Standalones

  * `shallowflow.base.standalones.SetVariable`

* Sources

  * `shallowflow.base.sources.DirectoryLister`
  * `shallowflow.base.sources.FileSupplier`
  * `shallowflow.base.sources.ForLoop`
  * `shallowflow.base.sources.GetStorage`
  * `shallowflow.base.sources.GetVariable`
  * `shallowflow.base.sources.ListStorage`
  * `shallowflow.base.sources.ListVariables`
  * `shallowflow.base.sources.Start`
    
* Transformers

  * `shallowflow.base.transformers.IncStorage`
  * `shallowflow.base.transformers.IncVariable`
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

  * `shallowflow.base.help.Markdown` - generates help in Markdown
  * `shallowflow.base.help.PlainText` - plain text help
