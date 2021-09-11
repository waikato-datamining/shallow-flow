import os
from shallowflow.api.io import File
from shallowflow.base.controls import Flow, run_flow
from shallowflow.base.sources import FileSupplier
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.sklearn.estimators import GenericConfiguration
from shallowflow.sklearn.transformers import DatasetLoader, TrainClassifier
from shallowflow.sklearn.transformers.datasetloaders import ArffLoader

flow = Flow().manage([
    FileSupplier({"files": [File("./data/iris.arff")]}),
    DatasetLoader({"loader": ArffLoader({"class_index": "last"})}),
    TrainClassifier({"estimator": GenericConfiguration({"class_name": "sklearn.ensemble.RandomForestClassifier", "options": {"n_estimators": 50, "max_leaf_nodes": 5}})}),
    ConsoleOutput()
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
