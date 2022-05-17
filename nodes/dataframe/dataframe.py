import pandas
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../utils")
import utils
import importlib

importlib.reload(utils)

# define processing function
def process_input(kwargs, config, topic, payload):
    # load data from request
    df = pandas.read_json(payload, orient="values")

    # Get the rules from the configuration
    rules = config["rules"]
    for rule in rules:
        column = rule["c"]
        type = rule["t"]

        # retype column
        dtype = {}
        dtype[column] = type
        df = df.astype(dtype)

        # set index column if found
        if bool(rule["i"]):
            df = df.set_index(column)

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

    # Create a file with the name of the node
    file = config["id"] + ".pickle"
    path = config["path"]
    fullname = os.path.join(path, file)
    df.to_pickle(fullname)

    return fullname, "dataframe", "done"


# Process input
utils.wait_for_input(process_input)
