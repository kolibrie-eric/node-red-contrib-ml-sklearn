# Dependencies

These nodes depend on python 3, pandas and scikit-learn being pre-installed. The versions tested are:

- python 3.7.3
- pandas 1.3.5
- numpy 1.20.2
- scikit-learn 1.0.2

If you install the nodes on a raspberry pi, make sure to uninstall the python3-pandas and python3-numpy packages:

<code>apt-get purge python3-pandas python3-numpy</code>

and install the required packages with pip (assuming pip is an alias for pip3). Warning this may take some time depending on your pi's version!

<code>apt-get install python3-pip  
python -m pip install numpy  
python -m pip install pandas  
python -m pip install scikit-learn</code>
