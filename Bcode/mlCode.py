import sklearn
import pickle as pkl
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.model_selection import train_test_split,GridSearchCV,RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier,VotingClassifier
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix,roc_curve,roc_auc_score, auc,classification_report
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE,RandomOverSampler
import numpy as np
from scipy.stats import uniform, randint
import pandas as pd
from sklearn.feature_selection import chi2,f_classif,SelectKBest,SelectPercentile,mutual_info_classif, RFE


def data_encoder(instrument_readings_df):
  X = instrument_readings_df.drop(columns = ['Product ID'])
  with open (r'D:\fp_ml\Instrument-failure-prediction\model\scaler.pkl', 'rb') as f:
    Type_data = pkl.load(f)
  encoder =  LabelEncoder().fit(Type_data)
  X['Type'] = encoder.transform(instrument_readings_df['Type'])
  return X

def data_engineering(instrument_readings):
  #UDI,Product ID,Type,Air temperature [K],Process temperature [K],Rotational speed [rpm],Torque [Nm],Tool wear [min],Noise Power,Noise,Difference Temperature
  instrument_readings_df = pd.DataFrame([instrument_readings])
  instrument_readings_df['Noise Power'] = (2*np.pi*instrument_readings_df['Rotational speed [rpm]']*instrument_readings_df['Torque [Nm]'])/60
  instrument_readings_df['Noise'] = instrument_readings_df['Noise Power'] - 2860
  instrument_readings_df['Difference Temperature'] =  (instrument_readings_df['Process temperature [K]'] - instrument_readings_df['Air temperature [K]'])/2
  instrument_readings_df[['Noise Power','Noise']] = instrument_readings_df[['Noise Power','Noise']].round(2)
  instrument_readings_df['Rotation per torque'] = instrument_readings_df['Rotational speed [rpm]']/instrument_readings_df['Torque [Nm]']
  instrument_readings_df['Torque per Rotation'] = instrument_readings_df['Torque [Nm]']/instrument_readings_df['Rotational speed [rpm]']
  instrument_readings_df['Tool wear per Rotation'] = instrument_readings_df['Tool wear [min]']/instrument_readings_df['Rotational speed [rpm]']
  instrument_readings_df['Tool wear per torque'] = instrument_readings_df['Tool wear [min]']/instrument_readings_df['Torque [Nm]']
  instrument_readings_df['Tool wear per power'] = instrument_readings_df['Tool wear [min]']/instrument_readings_df['Noise Power']
  return instrument_readings_df

def FailureType_decoder(failure_type_encoded):
  with open(r'D:\fp_ml\Instrument-failure-prediction\model\FailureType.pkl','rb') as f:
    Failure_types = pkl.load(f)
  decoder = LabelEncoder().fit(Failure_types)
  Failure_Type_decoded = decoder.inverse_transform(failure_type_encoded)
  return Failure_Type_decoded

def IFDS_model(instrument_readings):
  with open (r'D:\fp_ml\Instrument-failure-prediction\model\model_smote.pkl','rb')as file:
    ensemble_smote = pkl.load(file)
  with open (r'D:\fp_ml\Instrument-failure-prediction\model\model_rose.pkl','rb')as file:
    ensemble_rose = pkl.load(file)

  data_engineered_instrument_readings = data_engineering(instrument_readings)
  X = data_encoder(data_engineered_instrument_readings)

  y_pred_smote = ensemble_smote.predict_proba(X)
  y_pred_rose = ensemble_rose.predict_proba(X)

  avr_proba = (y_pred_smote + y_pred_rose)/2
  y_pred = np.argmax(avr_proba, axis =1)


  if y_pred:
    with open (r'D:\fp_ml\Instrument-failure-prediction\model\MultiClassModel.pkl','rb')as file:
      MultiClassModel = pkl.load(file)

    failure_type_encoded = MultiClassModel.predict(X)
    Failure_Type_decoded = FailureType_decoder(failure_type_encoded)

    result = f'❌Instrument is Failure due to {Failure_Type_decoded[0]}❌'

  else:
    result = '✅No Failure✅'

  return result

