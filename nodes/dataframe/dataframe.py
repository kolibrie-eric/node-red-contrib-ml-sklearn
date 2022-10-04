import pandas as pd
import os
import sys

pd.set_option("display.max_columns", None)
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../utils")
import utils

# define processing function
def dataframe_process_input(kwargs, config, topic, payload):
    # load data from request
    df = pd.read_json(payload, orient=config["orient"])

    # Do we need to show intermediate debug information?
    debug = config["debug"] == True

    # Get the rules from the configuration
    rules = config["rules"]

    for rule in rules:
        column = rule["c"]
        type = rule["t"]

        # retype column
        dtype = {}
        dtype[column] = type
        df = df.astype(dtype)

        if debug:
            utils.debug(None, f"Retyping colum {column} to {type}")

        # set index column if found
        if bool(rule["i"]):
            df = df.set_index(column)
            if debug:
                utils.debug(None, f"Using column {column} as index")

    # Do column shift
    # for rule in rules:
    #     column = rule["c"]
    #     # shift column if specified
    #     if rule["s"]:
    #         shift = int(rule["s"])
    #         if not shift == 0:
    #             # Remove all columns but the column to shift from the dataframe
    #             columns = df.columns.values.tolist()
    #             if column in columns:
    #                 columns.remove(column)
    #             df_shift = df.drop(columns=columns)
    #             # df_shift = df_shift.shift(shift)
    #             # print(df_shift)
    if debug:
        utils.debug("dtypes", df.dtypes)
        utils.debug("head(5)", df.head())

    # Create a file with the name of the node
    file = config["id"] + ".pickle"
    path = config["path"]
    fullname = os.path.join(path, file)
    df.to_pickle(fullname)

    if debug:
        utils.debug("path", fullname)

    # Return payload, topic and final status
    return fullname, "dataframe", "done"


# Process input
utils.wait_for_input(dataframe_process_input)
