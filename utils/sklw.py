import pickle
import os
import utils
import json
import numpy
from inspect import signature
import sys

# Sklearn classes
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC


class sklw:
    def _initialize_model(self, algorithm, **kwargs):
        """
        Filter incoming parameters based on the specified algorithm to match the signature of the model' constructor
        Any parameter that is not a constructor parameter will be ignored

        Args:
            algorithm: The name of the algorithm to initialize the model with, e.g. a decision tree, support vector or random forest regressor or classifier
            kwargs: A dictionary of key, value pairs that contain the parameters as passed to this method via the message object in nodered or via the node configuration
        """
        # Create the model from its name/string
        model = getattr(sys.modules[__name__], algorithm)

        # get the parameters for the constructor
        params = list(signature(model).parameters)

        # gather parameters that are in the list of parameters for the algorithm' constructor
        params = {k: v for k, v in kwargs.items() if k in params}

        # instantiate the model
        self.model = model(**params)

    def __init__(self, config, algorithm=None, **kwargs):
        """
        Construct a wrapper around one of the Sklearn regressor or classifier classes.

        Args:
            config: The configuration of the node as passed by nodered to this constructor
            algorithm: The name of the Sklearn class to wrap, e.g. RandomForestRegressor. If not specified the constructor will
                try to load the model from a pickle file. The name of the file is part of the node configuration.
            kwargs: a dictionary of message parameters and configuration parameters containing the Sklearn class constructor parameters
                The dictionary may contain more than just the constructor parameters. Those will be ignored.
        """
        self.config = config
        self.path = self.config["path"]

        if algorithm is not None:
            self._initialize_model(algorithm, **kwargs)
        else:
            file = self.config["file"]
            self.last = os.stat(file).st_mtime
            self.model = pickle.load(open(file, "rb"))

        # type(model.model).__name__
        self.name = algorithm

    def fit(self, x, y=None):
        """
        Execute the fit method of the wrapped SKlearn class.
        """
        if y is not None:
            self.model.fit(x, y)
        else:
            self.model.fit(x)

        return self.save(self.model)

    def save(self, obj):
        # Create a file with the name of the node
        file = self.config["id"] + ".pickle"
        fullname = os.path.join(self.path, file)
        pickle.dump(obj, open(fullname, "wb"))
        return fullname

    def predict(self, x):
        return self.model.predict(x).tolist()

    def update(self):
        file = self.config["file"]
        modified = os.stat(file).st_mtime
        if modified > self.last:
            self.last = modified
            self.model = pickle.load(open(file, "rb"))

    def get_params(self, deep=True):
        return self.model.get_params(deep)

    def get_attribute(self, name):
        if hasattr(self.model, name):
            return getattr(self.model, name)
        return None

    def store_attributes(self, parameters):
        for var in dir(self.model):
            try:
                # Skip depracated attributes
                if var == "n_features_":
                    continue

                # Skip also everything starting with _
                if var.startswith("_"):
                    continue

                val = getattr(self.model, var)

                # Convert numpy array to a list
                if isinstance(val, numpy.ndarray):
                    val = val.tolist()

                # Check if object is serializable
                json.dumps(val)

                # Add attribute to parameters dictionary
                parameters[var] = val
            finally:
                continue
