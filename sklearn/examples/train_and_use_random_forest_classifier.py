import os
from shallowflow.api.io import File
from shallowflow.base.controls import Flow, run_flow, Trigger
from shallowflow.base.sources import FileSupplier, GetStorage, Start
from shallowflow.base.transformers import SetStorage
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.sklearn.estimators import GenericConfiguration
from shallowflow.sklearn.transformers import DatasetLoader, TrainSupervisedEstimator, SupervisedScoring
from shallowflow.sklearn.transformers.datasetloaders import ArffLoader

flow = Flow().manage([
    Start(),
    Trigger({"name": "load dataset"}).manage([
        FileSupplier({"files": [File("./data/iris.arff")]}),
        DatasetLoader({"loader": ArffLoader({"class_index": "last"})}),
        SetStorage({"storage_name": "dataset"})
    ]),
    Trigger({"name": "train"}).manage([
        GetStorage({"storage_name": "dataset"}),
        TrainSupervisedEstimator({"estimator": GenericConfiguration({"class_name": "sklearn.ensemble.RandomForestClassifier", "options": {"n_estimators": 50, "max_leaf_nodes": 5}})}),
        SetStorage({"storage_name": "estimator"})
    ]),
    Trigger({"name": "predict"}).manage([
        GetStorage({"storage_name": "dataset"}),
        SupervisedScoring({"storage_name": "estimator", "scores": True, "probabilities": True}),
        ConsoleOutput(),
    ])
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
