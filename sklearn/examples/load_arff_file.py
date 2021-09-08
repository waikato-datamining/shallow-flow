import os
from shallowflow.api.io import File
from shallowflow.base.controls import Flow, run_flow
from shallowflow.base.sources import FileSupplier
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.sklearn.transformers import DatasetLoader
from shallowflow.sklearn.transformers.datasetloaders import ArffLoader

flow = Flow().manage([
    FileSupplier({"files": [File("./data/iris.arff")]}),
    DatasetLoader({"loader": ArffLoader({"class_index": "last"})}),
    ConsoleOutput()
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
