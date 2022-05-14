import json
import pickle
import pandas
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../utils")
from sklw import SKLW
import utils
import importlib

importlib.reload(utils)

OUTLIER_DETECTORS = [
    "elliptic-envelope",
    "isolation-forest",
    "one-class-support-vector",
]

# define processing function
def process_input(kwargs, config, payload):
    try:
        # Try to load the data from file. Sometimes the payload is wrapped in "". Remove those
        file = payload.replace('"', "")
        store = pandas.HDFStore(file)
        df = store["df"]
        # os.chdir(cd)
    except Exception as e:
        # load data from request
        df = pandas.read_json(payload, orient="values")

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

    # Train the model and send the result. The first return value (payload) is the file name of trained model.
    # The second one (topic), the name of the model/algorithm used
    return algorithm.fit(x, y), config["algorithm"]


# Process input
utils.wait_for_input(process_input)
