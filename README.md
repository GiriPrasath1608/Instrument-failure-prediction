# Predictive Maintenance for Manufacturing Equipment

https://giriprasath1608-instrument-failure-prediction-home-hictyt.streamlit.app/ deployed in streamlit cloud community server

## Project Description
The goal is to develop a predictive maintenance model that can predict equipment
failures before they occur. The dataset includes sensor readings and maintenance
logs from a variety of machines.

## Business Use Cases:
1. **Cost Reduction**: Minimize downtime and reduce maintenance costs by
predicting equipment failures in advance.
2. **Efficiency Improvement**: Increase operational efficiency by scheduling
maintenance at optimal times.
3. **Asset Management**: Extend the lifespan of equipment by preventing
unexpected breakdowns.
4. **Safety Enhancement**: Improve workplace safety by addressing potential
equipment failures proactively.

## Data Set Explanation:
The dataset consists of 10 000 data points stored as rows with 14 features in columns
1. **UID**: unique identifier ranging from 1 to 10000
2. **ProductID**: consisting of a letter L, M, or H for low (50% of all products), medium (30%),
and high (20%) as product quality variants and a variant-specific serial number
3. **Air temperature [K]**: generated using a random walk process later normalized to a standard
deviation of 2 K around 300 K
4. **Process temperature [K]**: generated using a random walk process normalized to a standard
deviation of 1 K, added to the air temperature plus 10 K.
5. **Rotational speed [rpm]**: calculated from power of 2860 W, overlaid with a normally
distributed noise
6. torque [Nm]**: torque values are normally distributed around 40 Nm with an Ïƒ = 10 Nm and
no negative values.
7. **Tool wear [min]**: The quality variants H/M/L add 5/3/2 minutes of tool wear to the used tool
in the process. and a 'Machine failure' label that indicates whether the machine has failed in this particular data
point for any of the following failure modes is true.
8. **Target** : Failure or Not  
9. **Failure Type** : Type of Failure (There are two targets dont take
these as features)

## Installation
    To run the project, clone the repository and install the reuired dependencies:

    git clone https://github.com/GiriPrasath1608/Instrument-failure-prediction.git

    pip install -r requirements.txt

    Make sure you have Jupyter installed to run the notebooks.

## How to run the Project
1. After installing the dependencies, you can run the Jupyter notebook.
2. Open the notebook Preprocessing\FP_data_clean & model train.ipynb and run the cell to follow the analysis and model training.
3. The full analysis and code are available in the Jupyter Notebook.

## Result
### Target Result
    accuracy = 0.98
    precision = 0.85
    recall = 0.81
    specificity = 0.99
    f1 = 0.83
    auc_score = 0.98
### Failure Type Result
    accuracy = 0.98
    weighted avg = 0.99
