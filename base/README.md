# shallowflow-base
The base components for shallowflow.

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


## Examples

* [option handling](base/examples/option_handling.py)
* [finding modules/classes](base/examples/find_modules_and_classes.py)
* [listing files/dirs](base/examples/list_files.py)
* [listing files/dirs (flow)](base/examples/flow_listing_files.py)
* [stopping flow](base/examples/stopping_flow.py)
* [use variables](base/examples/use_variables.py)
* [use lists in variable](base/examples/use_lists_in_variable.py)
* [env variables](base/examples/env_var.py)
* [using branches](base/examples/branching.py)
* [while loop](base/examples/while_loop.py)
