# Available nodes

## Dataframe

The dataframe node is a wrapper around the pandas dataframe. It will take a payload of values and transform that into a dataframe. It currently supports
the following operations:

- Retype of a column (via [astype](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html))
- Column shift (via [shift](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.shift.html?highlight=pandas%20shift#pandas.DataFrame.shift))
- Set the index of the dataframe (via [set_index](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html))

The node will output the name of the pickle file it created after completing the transformation. The output can be forwarded to a regressor or classifier node
to train a model.

## Regressor

The regressor node wraps the following regression algorithms within the scikit learn package:

- DecisionTreeRegressor
- MLPRegressor
- RandomForestRegressor
- SVR
- KNeighborsRegressor

Depending on the algorithm chosen, the node allows you to configure one or more parameters to pass to its constructor. When a payload is passed to the node, it will
call the fit method of the algorithm. Upon success, its output is a pickle file containing the trained model. The node can be provided a payload in the form of a
dictionary or the name of a pickle file which is the output of the dataframe node.

Configured parameters can be overridden by a corresponding message property, e.g.:

<code>msg.n_estimators=200</code>

will override the n_estimators property configured for the RandmoForestRegressor.

## Classifier

The classifier node wraps the following classifier algorithms within the scikit learn package:

- DecisionTreeClassifier
- KNeighborsClassifier
- MLPClassifier
- RandomForestClassifier
- SVC

Its behavior is similar to the [regressor](#regressor) node.

# Dependencies

These nodes depend on python 3, pandas, numpy and scikit-learn being pre-installed. The packages are not installed by npm! The versions tested against are:

- python 3.7.3
- pandas 1.3.5
- numpy 1.20.2
- scikit-learn 1.0.2

If you install the nodes on a raspberry pi, make sure to first uninstall the _python3-pandas_ and _python3-numpy_ packages:

<code>apt-get purge python3-pandas python3-numpy</code>

and install the required packages with pip (where pip is an alias for pip3). Warning: this may take some time depending on your pi's version!

<code>apt-get install python3-pip</code>  
<code>apt-get install python3-setuptools</code>  
<code>python -m pip install numpy pandas scikit-learn</code>
