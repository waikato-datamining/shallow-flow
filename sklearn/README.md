# shallowflow-sklearn
[sklearn](https://github.com/andymccurdy/redis-py) components for shallowflow.

## Installation

Install via pip:

```commandline
pip install "git+https://github.com/waikato-datamining/shallowflow.git#egg=shallowflow-sklearn&subdirectory=sklearn"
```

## Actors

* Sources

  * `shallowflow.sklearn.sources.`

* Transformers

  * `shallowflow.sklearn.transformers.DatasetLoader`
  * `shallowflow.sklearn.transformers.SupervisedScoring`
  * `shallowflow.sklearn.transformers.TrainSupervisedEstimator`
  * `shallowflow.sklearn.transformers.TrainUnsupervisedEstimator`
  * `shallowflow.sklearn.transformers.UnsupervisedScoring`
    
* Sinks

  * `shallowflow.sklearn.sinks.`
 

## Examples

* [loading an ARFF file](examples/load_arff_file.py)
* [train RandomForest classifier](examples/train_random_forest_classifier.py)
* [train and use RandomForest classifier](examples/train_and_use_random_forest_classifier.py)
* [train KMeans clusterer](examples/train_kmeans_clusterer.py)
* [train and use KMeans clusterer](examples/train_and_use_kmeans_clusterer.py)
