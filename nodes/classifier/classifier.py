import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../utils")
from sklw import SKLW
import utils
import importlib

importlib.reload(utils)

# define processing function
def classifier_process_input(kwargs, config, topic, payload):
    # Get the x and y from the payload
    x, y = utils.read_data(payload)

    # Add the configuration parameters to the kwargs (constructor parameters) when specified
    # and not already present. The parameters in the message will override a configuration parameter with the same name
    utils.process_parameters(config, kwargs)

    # Construct the model
    model = None
    algorithm = config["algorithm"]
    if algorithm == "decision-tree-classifier":
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

    # Fill the parameters dictionary
    parameters = {}
    parameters["payload"] = model.fit(x, y)

    # Train the model and send the result. The first return value (payload) is the file name of trained model.
    # The second one (topic), the name of the model/algorithm used. The topic 'model' is used by the predictor
    # to store the trained model file for later use. The third parameter is the status of the node when training is succesful
    return parameters, "model", "training complete"


# Process input
utils.wait_for_input(classifier_process_input)
