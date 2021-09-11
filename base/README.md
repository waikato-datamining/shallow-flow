# shallowflow-base
The base components for shallowflow.

## Actors

* Control actors

  * `shallowflow.base.controls.Branch`
  * `shallowflow.base.controls.ConditionalTee`
  * `shallowflow.base.controls.ConditionalTrigger`
  * `shallowflow.base.controls.ContainerValuePicker`
  * `shallowflow.base.controls.Flow`
  * `shallowflow.base.controls.Sequence`
  * `shallowflow.base.controls.Sleep`
  * `shallowflow.base.controls.Stop`
  * `shallowflow.base.controls.Tee`
  * `shallowflow.base.controls.Trigger`
  * `shallowflow.base.controls.WhileLoop`

* Standalones

  * `shallowflow.base.standalones.CallableActors`
  * `shallowflow.base.standalones.SetVariable`

* Sources

  * `shallowflow.base.sources.CallableSource`
  * `shallowflow.base.sources.DirectoryLister`
  * `shallowflow.base.sources.FileSupplier`
  * `shallowflow.base.sources.ForLoop`
  * `shallowflow.base.sources.GetStorage`
  * `shallowflow.base.sources.GetVariable`
  * `shallowflow.base.sources.ListStorage`
  * `shallowflow.base.sources.ListVariables`
  * `shallowflow.base.sources.Start`
    
* Transformers

  * `shallowflow.base.transformers.CallableTransformer`
  * `shallowflow.base.transformers.IncStorage`
  * `shallowflow.base.transformers.IncVariable`
  * `shallowflow.base.transformers.PassThrough`
  * `shallowflow.base.transformers.SetStorage`
  * `shallowflow.base.transformers.SetVariable`
    
* Sinks

  * `shallowflow.base.sinks.CallableSink`
  * `shallowflow.base.sinks.ConsoleOutput`
  * `shallowflow.base.sinks.Null`

## Conditions

* `shallowflow.base.conditions.AlwaysFalse`
* `shallowflow.base.conditions.AlwaysTrue`
* `shallowflow.base.conditions.NumExpr`

## Help

  * `shallowflow.base.help.Markdown` - generates help in Markdown
  * `shallowflow.base.help.PlainText` - plain text help


## Examples

* [option handling](examples/option_handling.py)
* [finding modules/classes](examples/find_modules_and_classes.py)
* [listing files/dirs](examples/list_files.py)
* [compatibility](examples/comp.py)
* [listing files/dirs (flow)](examples/flow_listing_files.py)
* [stopping flow](examples/stopping_flow.py)
* [use variables](examples/use_variables.py)
* [use lists in variable](examples/use_lists_in_variable.py)
* [env variables](examples/env_var.py)
* [using branches](examples/branching.py)
* [while loop](examples/while_loop.py)
* [using callable actors](examples/callable_actors.py)
