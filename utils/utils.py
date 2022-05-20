import sys
import json
import pandas


def wait_for_input(process_input):
    """Input processing function

    The function is a mirror of the interprocess communication implemented by utils.js. It first expects to receive the node configuration
    and then will wait for ever for message input.

    In case the node's processing function generates an exception, the exception is caught and send to the error output of the process.

    The output is send as a JSON string to the standard output of the process (stdout)

    Args:
        process_input: the processing function for the node, e.g. process_input in classifier.py
        The processing function returns a tuple: parameters, topic and status. The parameters and topic are passed to the output message of the node,
        where each of the entries in the parameters dictionary is added as a separate
        The status is used as the status text of the node.
    """
    # read configurations
    config = json.loads(input())

    while True:
        # read request (wait forever until input is provided)
        data = json.loads(input())

        try:
            # Retrieve the arguments send by 'utils.js'
            kwargs = data["kwargs"]
            payload = data["payload"]
            topic = data["topic"]

            # Process the data
            parameters, topic, status = process_input(kwargs, config, topic, payload)

            # compile the result message
            msg = {}
            if parameters:
                for key in parameters:
                    msg[key] = parameters[key]
            else:
                msg["payload"] = None
            msg["topic"] = topic
            msg["status"] = status

            # And send it back to the 'utils.js' script
            print(json.dumps(msg), file=sys.stdout)
        except Exception as e:
            # Print exceptions to the stderr output but continue processing input
            print(e, file=sys.stderr)


def read_data(payload):
    """Read the data from the payload and return the x and y data

    The function will first try use the payload as the name of a file, assuming the data to load is in that file.
    If unsuccesfull, the payload is than used as a JSON dictionary, holding the data

    When loaded, a dataframe is used to hold the x and y data, where the assumption is that the last column is the y-column.

    Args:
        payload: The name of (pickle) file holding the data to read or a JSON dictionary.

    Returns:
        the x and y columns of the dataframe loaded
    """
    df = None
    try:
        # Try to load the data from file. Sometimes the payload is wrapped in "". Remove those
        if payload[0] == '"':
            payload = payload[1 : len(payload) - 1]
        df = pandas.read_pickle(payload)
    except Exception as e:
        # load data from msg.payload
        df = pandas.read_json(payload, orient="values")

    # Determine the features and the y-column
    x = df.iloc[:, :-1]  # Everything but the last column
    y = df.iloc[:, -1]  # Last column

    return x, y


def process_parameters(config, kwargs):
    """Process the configuration parameters

    The function will add all parameters found in the config["parameter"] dictionary, not already present in the kwargs.

    Args:
        config: The node configuration dictionary (see the javascript file per node, e.g. regressor.js)
        kwargs: The set of arguments that will be passed to the model constructor, e.g. RandomForestRegressor
    """

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
                    kwargs[parameter] = cast(val, type)


def cast(val, type):
    """Cast the value received to the specified python type

    All scikit learn constructors expect a typed parameter, hence passing it a string value will throw an exception
    In some cases a parameter can be of type int, float or string depending on its use

    The function will try to infer the type, when a multi-type parameter is specified, e.g. int-float. If the value
    contains a decimal point, the type is assumed to be a float else an integer.

    Args:
        val: A string value that will be casted
        type: The type to cast to, e.g. int for a Python int, or string for a Python str

    Returns:
        The value cast to the specified type, if the type is known, else just the value
    """
    if type == "float":
        val = float(val)
    elif type == "int":
        val = int(val)
    elif type == "bool":
        val = bool(val)
    elif type == "int-float":
        if "." in val:
            val = float(val)
        else:
            val = int(val)
    elif type == "int-string":
        try:
            val = int(val)
        except:
            val = str(val)
    elif type == "float-string":
        try:
            val = float(val)
        except:
            val = str(val)
    elif type == "int-float-string":
        try:
            if "." in val:
                val = float(val)
            else:
                val = int(val)
        except:
            val = str(val)
    elif type == "dict":
        val = json.loads(val)
    elif type == "dict-string":
        try:
            val = json.loads(val)
        except:
            val = str(val)
    return val
