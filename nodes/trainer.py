import json
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
def process_input(kwargs, config, topic, payload):
    try:
        # Try to load the data from file. Sometimes the payload is wrapped in "". Remove those
        if payload[0] == '"':
            payload = payload[1 : len(payload) - 1]
        df = pandas.read_pickle(payload)
        # df = store["df"]
        # os.chdir(cd)
    except Exception as e:
        # load data from request
        df = pandas.read_json(payload, orient="values")

    # The outlier algorithms expect the full dataframe
    algorithm = config["algorithm"]
    if algorithm in OUTLIER_DETECTORS:
        x = df
        y = None
    else:
        x = df.iloc[:, :-1]  # Everything but the last column
        y = df.iloc[:, -1]  # Last column

    # Go through the parameters passed via the configuration. If not in kwargs yet, add them
    for item in config["parameters"]:
        parameter = None
        type = None
        for key, val in item.items():
            if key == "p":
                # val contains the value of 'p', e.g. n_estimators
                if not val in kwargs:
                    # Extract type information
                    parameter = val.split(":")
                    if len(parameter) > 1:
                        type = parameter[1]
                    parameter = parameter[0]
            else:
                # val contains the value of 'v', the value of the parameter
                # type contains the type of value to pass to the constructor
                if parameter:
                    kwargs[parameter] = utils.cast(val, type)

    model = None
    if algorithm == "elliptic-envelope":
        from sklearn.covariance import EllipticEnvelope

        model = SKLW(config, model=EllipticEnvelope(**kwargs))
    elif algorithm == "isolation-forest":
        from sklearn.ensemble import IsolationForest

        model = SKLW(config, model=IsolationForest(**kwargs))
    elif algorithm == "one-class-support-vector":
        from sklearn.svm import OneClassSVM

        model = SKLW(config, model=OneClassSVM(**kwargs))
    elif algorithm == "decision-tree-classifier":
        from sklearn.tree import DecisionTreeClassifier

        model = SKLW(config, model=DecisionTreeClassifier(**kwargs))
    elif algorithm == "k-neighbors-classifier":
        from sklearn.neighbors import KNeighborsClassifier

        model = SKLW(config, model=KNeighborsClassifier(**kwargs))
    elif algorithm == "multi-layer-perceptron-classifier":
        from sklearn.neural_network import MLPClassifier

        model = SKLW(config, model=MLPClassifier(**kwargs))
    elif algorithm == "random-forest-classifier":
        from sklearn.ensemble import RandomForestClassifier

        model = SKLW(config, model=RandomForestClassifier(**kwargs))
    elif algorithm == "support-vector-classifier":
        from sklearn.svm import SVC

        model = SKLW(config, model=SVC(**kwargs))
    elif algorithm == "decision-tree-regressor":
        from sklearn.tree import DecisionTreeRegressor

        model = SKLW(config, model=DecisionTreeRegressor(**kwargs))
    elif algorithm == "multi-layer-perceptron-regressor":
        from sklearn.neural_network import MLPRegressor

        model = SKLW(config, model=MLPRegressor(**kwargs))
    elif algorithm == "random-forest-regressor":
        from sklearn.ensemble import RandomForestRegressor

        model = SKLW(config, model=RandomForestRegressor(**kwargs))
    elif algorithm == "support-vector-regressor":
        from sklearn.svm import SVR

        model = SKLW(config, model=SVR(**kwargs))
    elif algorithm == "k-neighbors-regressor":
        from sklearn.neighbors import KNeighborsRegressor

        model = SKLW(config, model=KNeighborsRegressor(**kwargs))

    # Train the model and send the result. The first return value (payload) is the file name of trained model.
    # The second one (topic), the name of the model/algorithm used
    return model.fit(x, y), "model", "training complete"


# Process input
utils.wait_for_input(process_input)
