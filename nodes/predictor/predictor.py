import pandas as pd
import os
import sys
import pickle

pd.set_option("display.max_columns", None)
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../utils")
import utils

# define processing function
def predictor_process_input(kwargs, config, topic, payload):
    # Do we need to show intermediate debug information?
    # debug = config["debug"] == True
    # utils.debug(debug)

    # The file containing the name of the training data file
    file = config["id"] + ".pickle"
    fullname = os.path.join(config["path"], file)

    # Sometimes the payload is wrapped in "". Remove those
    if payload[0] == '"':
        payload = payload[1 : len(payload) - 1]

    # If we received a trained model file, save that for later use
    if topic == "model":
        pickle.dump(payload, open(fullname, "wb"))
        # if debug:
        #     utils.debug("model saved", fullname)
        return None, None, "model received"

    # load data from request
    try:
        # Try to load the data from file.
        df = pd.read_pickle(payload)
    except Exception as e:
        # load data from request
        df = pd.read_json(payload, orient="values")

    # By now we should have received a training model file or one was
    # previously stored on disk and now we have a payload to process
    if not os.path.exists(fullname):
        raise Exception("No training model found")
    file = pickle.load(open(fullname, "rb"))

    # Initialize the model. SKLW expects the filename to be part of the configuration
    config["file"] = file
    model = utils.sklw(config)

    # Make the prediction and get the result. The first return value (payload) is the prediction.
    # The second one (topic), the name of the model/algorithm used
    df[config["y_column"]] = model.predict(df)
    parameters = {}
    parameters["payload"] = df.to_json(orient=config["orient"])

    # add the attributes of the model to the message
    model.store_attributes(parameters)

    # Return payload, topic and final status
    return parameters, "prediction", "prediction complete"


# Process input
utils.wait_for_input(predictor_process_input)
