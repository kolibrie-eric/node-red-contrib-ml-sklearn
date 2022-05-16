import json
import pandas
import os
import sys
import pickle

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../utils")
from sklw import SKLW
import utils
import importlib

importlib.reload(utils)

# define processing function
def process_input(kwargs, config, topic, payload):
    # The file containing the name of the training data file
    file = config["id"] + ".pickle"
    fullname = os.path.join(config["path"], file)

    # Sometimes the payload is wrapped in "". Remove those
    if payload[0] == '"':
        payload = payload[1 : len(payload) - 1]

    # If we received a trained model file, save that for later use
    if topic == "model":
        pickle.dump(payload, open(fullname, "wb"))
        return None, None, "model received"

    # load data from request
    try:
        # Try to load the data from file.
        df = pandas.read_pickle(payload)
    except Exception as e:
        # load data from request
        df = pandas.read_json(payload, orient="values")

    # By now we should have received a training model file or one was
    # previously stored on disk and now we have a payload to process
    if not os.path.exists(fullname):
        raise Exception("No training model found")
    file = pickle.load(open(fullname, "rb"))

    # Initialize the model. SKLW expects the filename to be part of the configuration
    config["file"] = file
    model = SKLW(config)

    # Make the prediction and send the result. The first return value (payload) is the prediction.
    # The second one (topic), the name of the model/algorithm used
    columns = df.columns
    df[config["y_column"]] = model.predict(df)
    payload = df.to_json(orient=config["orient"])

    return payload, type(model.model).__name__, "prediction complete"


# Process input
utils.wait_for_input(process_input)
