import os
from shallowflow.api.io import File
from shallowflow.base.controls import Flow, run_flow, Trigger
from shallowflow.base.sources import FileSupplier, Start, GetStorage
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.base.transformers import SetStorage
from shallowflow.sklearn.estimators import GenericConfiguration
from shallowflow.sklearn.transformers import DatasetLoader, TrainUnsupervisedEstimator, UnsupervisedScoring
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
        TrainUnsupervisedEstimator({"estimator": GenericConfiguration({"class_name": "sklearn.cluster.KMeans", "options": {"n_clusters": 3}})}),
        SetStorage({"storage_name": "estimator"})
    ]),
    Trigger({"name": "predict"}).manage([
        GetStorage({"storage_name": "dataset"}),
        UnsupervisedScoring({"storage_name": "estimator"}),
        ConsoleOutput(),
    ])
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
