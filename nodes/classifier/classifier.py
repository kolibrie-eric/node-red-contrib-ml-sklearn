import os
import sys
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

pd.set_option("display.max_columns", None)
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../utils")
import utils

# define processing function
def classifier_process_input(kwargs, config, topic, payload):
    # Do we need to show intermediate debug information?
    debug = config["debug"] == True

    # Get the x and y from the payload
    X, y = utils.read_data(payload, debug)
    if debug:
        utils.debug("X", X)
        utils.debug("y", y)

    # Add the configuration parameters to the kwargs (constructor parameters) when specified
    # and not already present. The parameters in the message will override a configuration parameter with the same name
    utils.process_parameters(config, kwargs)

    # Pass only the arguments known to this algorithm
    algorithm = config["algorithm"]
    if debug:
        utils.debug("algorithm", algorithm)

    # Construct the model
    model = utils.sklw(config, algorithm, **kwargs)
    if debug:
        utils.debug("model-parameters", model.get_params())

    # Train the model
    parameters = {}
    parameters["payload"] = model.fit(X, y) if model else None

    # add the attributes of the model to the message
    model.store_attributes(parameters)

    # Return the message parameters, topic and final status
    return parameters, "model", "training complete"


# Process input
utils.wait_for_input(classifier_process_input)
