import json
import pandas
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../utils")
from sklw import SKLW
import utils
import importlib

importlib.reload(utils)

# define processing function
def process_input(kwargs, config, payload):
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

    # Initialize the model
    config["file"] = kwargs["modelfile"]
    model = SKLW(config)

    # Make the prediction and send the result. The first return value (payload) is the prediction.
    # The second one (topic), the name of the model/algorithm used
    return model.predict(df), type(model.model).__name__


# Process input
utils.wait_for_input(process_input)
