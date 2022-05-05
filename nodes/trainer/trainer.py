import json
import pickle
import pandas
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../utils")
from sklw import SKLW

OUTLIER_DETECTORS = [
    "elliptic-envelope",
    "isolation-forest",
    "one-class-support-vector",
]

# read configurations
config = json.loads(input())

while True:
    # read request (wait forever until input is provided)
    data = json.loads(input())
    kwargs = data["kwargs"]
    payload = data["payload"]

    # load data from request
    df = pandas.read_json(payload, orient="values")

    # Check if we need to retype one or more columens
    if "astype" in kwargs:
        try:
            arg = json.loads(kwargs["astype"])
        except:
            arg = kwargs["astype"]
        df = df.astype(dtype=arg)
        del kwargs["astype"]

    # Reindex the dataframe if an index column is specified
    if "index" in kwargs:
        index_column = kwargs["index"]
        df = df.set_index(index_column)
        del kwargs["index"]

    # The outlier algorithms expect the full dataframe
    if config["algorithm"] in OUTLIER_DETECTORS:
        x = df
        y = None
    else:
        x = df.iloc[:, :-1]  # Everything but the last column
        y = df.iloc[:, -1]  # Last column

    algorithm = None

    if config["algorithm"] == "elliptic-envelope":
        from sklearn.covariance import EllipticEnvelope

        algorithm = SKLW(config, model=EllipticEnvelope(**kwargs))
    elif config["algorithm"] == "isolation-forest":
        from sklearn.ensemble import IsolationForest

        algorithm = SKLW(config, model=IsolationForest(**kwargs))
    elif config["algorithm"] == "one-class-support-vector":
        from sklearn.svm import OneClassSVM

        algorithm = SKLW(config, model=OneClassSVM(**kwargs))
    elif config["algorithm"] == "decision-tree-classifier":
        from sklearn.tree import DecisionTreeClassifier

        algorithm = SKLW(config, model=DecisionTreeClassifier(**kwargs))
    elif config["algorithm"] == "deep-neural-network-classifier-tensorflow":
        from dnnctf import DNNCTF

        algorithm = DNNCTF(config, del_prev_mod=True, **kwargs)
    elif config["algorithm"] == "k-neighbors-classifier":
        from sklearn.neighbors import KNeighborsClassifier

        algorithm = SKLW(config, model=KNeighborsClassifier(**kwargs))
    elif config["algorithm"] == "multi-layer-perceptron-classifier":
        from sklearn.neural_network import MLPClassifier

        algorithm = SKLW(config, model=MLPClassifier(**kwargs))
    elif config["algorithm"] == "random-forest-classifier":
        from sklearn.ensemble import RandomForestClassifier

        algorithm = SKLW(config, model=RandomForestClassifier(**kwargs))
    elif config["algorithm"] == "support-vector-classifier":
        from sklearn.svm import SVC

        algorithm = SKLW(config, model=SVC(**kwargs))
    elif config["algorithm"] == "decision-tree-regressor":
        from sklearn.tree import DecisionTreeRegressor

        algorithm = SKLW(config, model=DecisionTreeRegressor(**kwargs))
    elif config["algorithm"] == "multi-layer-perceptron-regressor":
        from sklearn.neural_network import MLPRegressor

        algorithm = SKLW(config, model=MLPRegressor(**kwargs))
    elif config["algorithm"] == "random-forest-regressor":
        from sklearn.ensemble import RandomForestRegressor

        algorithm = SKLW(config, model=RandomForestRegressor(**kwargs))
    elif config["algorithm"] == "support-vector-regressor":
        from sklearn.svm import SVR

        algorithm = SKLW(config, model=SVR(**kwargs))
    elif config["algorithm"] == "k-neighbors-regressor":
        from sklearn.neighbors import KNeighborsRegressor

        algorithm = SKLW(config, model=KNeighborsRegressor(**kwargs))

    # train model
    file = algorithm.fit(x, y)

    # output a message containing the file name of the model and marking the training as completed
    msg = {}
    msg["payload"] = file
    msg["topic"] = config["algorithm"]
    print(json.dumps(msg))
