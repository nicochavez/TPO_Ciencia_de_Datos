import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import difflib

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
    df['n_dots'] = df['url'].str.count(r'\.')
    df['n_hypens'] = df['url'].str.count(r'-')
    df['n_underline'] = df['url'].str.count(r'_')
    df['n_slash'] = df['url'].str.count(r'/')
    df['n_questionmark'] = df['url'].str.count(r'\?')
    df['n_equal'] = df['url'].str.count(r'=')
    df['n_at'] = df['url'].str.count(r'@')
    df['n_and'] = df['url'].str.count(r'&')
    df['n_exclamation'] = df['url'].str.count(r'!')
    df['n_space'] = df['url'].str.count(r' ')
    df['n_tilde'] = df['url'].str.count(r'~')
    df['n_comma'] = df['url'].str.count(r',')
    df['n_plus'] = df['url'].str.count(r'\+')
    df['n_asterisk'] = df['url'].str.count(r'\*')
    df['n_hastag'] = df['url'].str.count(r'#')
    df['n_dollar'] = df['url'].str.count(r'\$')
    df['n_percent'] = df['url'].str.count(r'%')
    
    return df


def similarityRate(urlPH):

    topWEBData = pd.read_csv('./datasets/TOP_Ranked_Websites_DataSet.csv')
    topWEBData = pd.DataFrame(topWEBData)
    topWEBData = topWEBData.Domain
    match = False
    similarSite = ""
    
    for site in topWEBData:
        if difflib.SequenceMatcher(None, site, urlPH).ratio() > 0.6:
            match = True
            similarSite = site
            break
            
    return similarSite

def blackListCheck(urlPH):
    blackList = pd.read_csv('./datasets/PhishTank-DataSet.csv')
    blackList = pd.DataFrame(blackList)
    blackList = blackList.url
    banned = False

    if urlPH in blackList.to_numpy():
        banned = True

    return banned

def complementaryPrediction(urlPH, prediction):

    finalPrediction = 0

    similar = similarityRate(urlPH)

    banned = blackListCheck(urlPH)

    print(similar)
    
    if similar != "" or banned or prediction == 1:
        finalPrediction = 1

    return finalPrediction


def groupBlackListCheck(dfURL):
    blackList = pd.read_csv('./datasets/PhishTank-DataSet.csv')
    blackList = pd.DataFrame(blackList)
    blackList = blackList.url
    blackList["prediction"] = 1
    banned = False

    dfPred = dfURL.join(blackList, 'url', 'url')
    dfPred.fillna(value=0, inplace=True)

    return dfPred


    







    
    
