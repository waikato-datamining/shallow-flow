import os
from shallowflow.api.io import File
from shallowflow.base.controls import Flow, run_flow, GetContainerValue
from shallowflow.base.sources import FileSupplier
from shallowflow.base.sinks import ConsoleOutput, PickledFileWriter
from shallowflow.sklearn.estimators import GenericConfiguration
from shallowflow.sklearn.transformers import DatasetLoader, TrainSupervisedEstimator
from shallowflow.sklearn.transformers.datasetloaders import ArffLoader

flow = Flow().manage([
    FileSupplier({"files": [File("./data/iris.arff")]}),
    DatasetLoader({"loader": ArffLoader({"class_index": "last"})}),
    TrainSupervisedEstimator({"estimator": GenericConfiguration({"class_name": "sklearn.ensemble.RandomForestClassifier", "options": {"n_estimators": 50, "max_leaf_nodes": 5}})}),
    GetContainerValue({"value_name": "estimator"}).manage([
        PickledFileWriter({"output_file": File("./output/rf.pkl")}),
    ]),
    ConsoleOutput({"prefix": "\n--> container\n"})
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
