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
save = config["save"]

while True:
    # read request
    data = input()
    try:
        # load data from request
        df = pandas.read_json(data, orient="values")
    except:
        # lead file specified in the request
        df = pandas.read_csv(json.loads(data)["file"], header=None)

    if config["algorithm"] in OUTLIER_DETECTORS:
        x = df
        y = None
    else:
        x = df.iloc[:, :-1]  # Everything but the last column
        y = df.iloc[:, -1]  # Last column

    algorithm = None

    if config["algorithm"] == "elliptic-envelope":
        from sklearn.covariance import EllipticEnvelope

        algorithm = SKLW(path=save, model=EllipticEnvelope(**config["kwargs"]))
    elif config["algorithm"] == "isolation-forest":
        from sklearn.ensemble import IsolationForest

        algorithm = SKLW(path=save, model=IsolationForest(**config["kwargs"]))
    elif config["algorithm"] == "one-class-support-vector":
        from sklearn.svm import OneClassSVM

        algorithm = SKLW(path=save, model=OneClassSVM(**config["kwargs"]))
    elif config["algorithm"] == "decision-tree-classifier":
        from sklearn.tree import DecisionTreeClassifier

        algorithm = SKLW(path=save, model=DecisionTreeClassifier(**config["kwargs"]))
    elif config["algorithm"] == "deep-neural-network-classifier-tensorflow":
        from dnnctf import DNNCTF

        algorithm = DNNCTF(path=save, del_prev_mod=True, **config["kwargs"])
    elif config["algorithm"] == "k-neighbors-classifier":
        from sklearn.neighbors import KNeighborsClassifier

        algorithm = SKLW(path=save, model=KNeighborsClassifier(**config["kwargs"]))
    elif config["algorithm"] == "multi-layer-perceptron-classifier":
        from sklearn.neural_network import MLPClassifier

        algorithm = SKLW(path=save, model=MLPClassifier(**config["kwargs"]))
    elif config["algorithm"] == "random-forest-classifier":
        from sklearn.ensemble import RandomForestClassifier

        algorithm = SKLW(path=save, model=RandomForestClassifier(**config["kwargs"]))
    elif config["algorithm"] == "support-vector-classifier":
        from sklearn.svm import SVC

        algorithm = SKLW(path=save, model=SVC(**config["kwargs"]))
    elif config["algorithm"] == "decision-tree-regressor":
        from sklearn.tree import DecisionTreeRegressor

        algorithm = SKLW(path=save, model=DecisionTreeRegressor(**config["kwargs"]))
    elif config["algorithm"] == "multi-layer-perceptron-regressor":
        from sklearn.neural_network import MLPRegressor

        algorithm = SKLW(path=save, model=MLPRegressor(**config["kwargs"]))
    elif config["algorithm"] == "random-forest-regressor":
        from sklearn.ensemble import RandomForestRegressor

        algorithm = SKLW(path=save, model=RandomForestRegressor(**config["kwargs"]))
    elif config["algorithm"] == "support-vector-regressor":
        from sklearn.svm import SVR

        algorithm = SKLW(path=save, model=SVR(**config["kwargs"]))

    try:
        # train model
        algorithm.fit(x, y)
    except Exception as e:
        print(e)
        raise ()

    print(config["algorithm"] + ": training completed.")
