from sklw import get_all_constructor_params
import json

# Get the name of the algorithm
algorithm = input()

# Get the constructor parameters for this algorithm
params = get_all_constructor_params(algorithm)

# Return the parameters to nodejs/nodered
print(json.dumps(params))
