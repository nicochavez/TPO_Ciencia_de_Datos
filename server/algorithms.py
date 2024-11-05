import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB

def get_MLNB():
    data_set = pd.read_csv('./datasets/DataSet_WebPhishing_Final.csv')

    dfWebPh = pd.DataFrame(data_set)

    #data_set_classification = pd.read_csv('/content/drive/MyDrive/Ciencia de Datos TPO/DataSets/URL Classification.csv', names=['url', 'category'])

    #dfWebClassification = pd.DataFrame(data_set_classification)


    #Separo DataSet en Etiquetas y columna de Clases (0 good / 1 bad)
    feature_cols = ['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash', 'n_questionmark', 'n_equal', 'n_at', 'n_and', 'n_exclamation', 'n_space', 'n_tilde', 'n_comma', 'n_plus', 'n_asterisk', 'n_hastag', 'n_dollar', 'n_percent']
    X = dfWebPh[feature_cols] # Etiquetas
    y = dfWebPh.phishing # Clases


    MLNB = MultinomialNB()

    MLNB.fit(X, y)

    return MLNB


def valueCalc(df):
  df['url_length'] = df['url'].str.len()
  df['n_dots'] = df['url'].str.count('\.')
  df['n_hypens'] = df['url'].str.count('-')
  df['n_underline'] = df['url'].str.count('_')
  df['n_slash'] = df['url'].str.count('/')
  df['n_questionmark'] = df['url'].str.count('\?')
  df['n_equal'] = df['url'].str.count('=')
  df['n_at'] = df['url'].str.count('@')
  df['n_and'] = df['url'].str.count('&')
  df['n_exclamation'] = df['url'].str.count('!')
  df['n_space'] = df['url'].str.count(' ')
  df['n_tilde'] = df['url'].str.count('~')
  df['n_comma'] = df['url'].str.count(',')
  df['n_plus'] =  df['url'].str.count('\+')
  df['n_asterisk'] = df['url'].str.count('\*')
  df['n_hastag'] = df['url'].str.count('#')
  df['n_dollar'] = df['url'].str.count('\$')
  df['n_percent'] = df['url'].str.count('%')
  df['n_hastag'] = df['url'].str.count('#')

  return(df)
