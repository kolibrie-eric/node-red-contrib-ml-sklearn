# SciKit-Learn models' wrapper
import pickle
import os


class SKLW:
    def __init__(self, config, model=None):
        self.config = config
        self.path = self.config["path"]

        if model is not None:
            self.model = model
        else:
            file = self.config["file"]
            self.last = os.stat(file).st_mtime
            self.model = pickle.load(open(file, "rb"))

    def fit(self, x, y=None):
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
