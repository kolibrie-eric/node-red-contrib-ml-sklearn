from pickle import TRUE


import sys
import json
import os


def wait_for_input(process_input):

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
            payload, topic, status = process_input(kwargs, config, topic, payload)

            # compile the result message
            msg = {}
            msg["payload"] = payload
            msg["topic"] = topic
            msg["status"] = status

            # And send it back to the 'utils.js' script
            print(json.dumps(msg), file=sys.stdout)
        except Exception as e:
            # Print exceptions to the stderr output but continue processing input
            print(e, file=sys.stderr)
