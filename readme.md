# Available nodes

## Dataframe

The dataframe node is a wrapper around the pandas dataframe. It will take a payload of values and transform that into a dataframe. It currently supports
the following operations:

- Retype of a column
- Column shift
- Set the index of the dataframe

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

# Dependencies

These nodes depend on python 3, pandas and scikit-learn being pre-installed. The versions tested are:

- python 3.7.3
- pandas 1.3.5
- numpy 1.20.2
- scikit-learn 1.0.2

If you install the nodes on a raspberry pi, make sure to uninstall the python3-pandas and python3-numpy packages:

<code>apt-get purge python3-pandas python3-numpy</code>

and install the required packages with pip (assuming pip is an alias for pip3). Warning this may take some time depending on your pi's version!

<code>apt-get install python3-pip</code>  
<code>python -m pip install numpy pandas scikit-learn</code>
