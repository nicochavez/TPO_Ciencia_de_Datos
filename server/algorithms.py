import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import difflib
import tldextract

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

    topWEBData = pd.read_csv('./datasets/top_websites.csv', delimiter=';')


    topWEBData = topWEBData['Domain']  # Asegúrate de que 'Domain' es el nombre correcto de la columna.
    match = False
    similarSite = ""
    
    for site in topWEBData:
        if difflib.SequenceMatcher(None, site, urlPH).ratio() > 0.8 or difflib.SequenceMatcher(None, site, urlPH).ratio() < 0.9:
            match = True
            similarSite = site
            break

    
    return similarSite

def blackListCheck(urlPH):
    blackList = pd.read_csv('./datasets/PhishTank-DataSet.csv')
    blackList = pd.DataFrame(blackList)
    blackList = blackList['url']
    banned = False

    if urlPH in blackList.to_numpy():
        banned = True

    return banned

def get_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def complementaryPrediction(urlPH, prediction):
    url_domain = get_domain(urlPH)

    finalPrediction = 0

    similar = similarityRate(url_domain)

    banned = blackListCheck(url_domain)

    print(similar)
    if len(similar) > 0:
        finalPrediction = 1

    return finalPrediction


def groupBlackListCheck(dfURL):
    blackList = pd.read_csv('./datasets/PhishTank-DataSet.csv')
    blackList = pd.DataFrame(blackList)
    blackList = blackList['url']
    banned = False
    blackList['prediction'] = 1  # Esto funciona si quieres asignar una columna "prediction" con valor 1.
    dfPred = pd.merge(dfURL, blackList[['url', 'prediction']], on='url', how='left')
    dfPred.fillna(value=0, inplace=True)


    return dfPred


    







    
    
