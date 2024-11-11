import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import difflib
import tldextract
import Levenshtein


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

def get_Similarity_Model():
    df = pd.read_csv('../datasets/Similarity_websites.csv')

    # Separar las características y la etiqueta
    X = df[["Min_Levenshtein_Distance"]]  # Convertir a DataFrame
    y = df["Phishing"]
    
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Crear y entrenar el modelo de Random Forest
    ranForest = RandomForestClassifier(random_state=42)
    ranForest.fit(X_train, y_train)
    

    return ranForest
    


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

def calculate_levenstein_distance(url):
    legit_domains = pd.read_csv('../datasets/top_websites.csv', delimiter=';')['Domain'].to_list()
    print(legit_domains)
    distances = [Levenshtein.distance(url, legit_domain) for legit_domain in legit_domains]
    return min(distances)



def blackListCheck(urlPH):
    blackList = pd.read_csv('./datasets/PhishTank-DataSet.csv')
    blackList = blackList['url']
    banned = False

    if urlPH in blackList.to_numpy():
        banned = True

    return banned

def get_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def prediction_by_characteristics(url):
    urlDict = {'url': [url]}
    urlDF = pd.DataFrame(urlDict)

    urlDF = valueCalc(urlDF)

    urlDF = urlDF.drop(columns=['url'])

    MLNB = get_MLNB()

    prediction = MLNB.predict(urlDF)

    return prediction[0]

def prediction_by_similarity(url):
    url_domain = get_domain(url)
    print(url_domain)
    ranForest = get_Similarity_Model()
    similarity = calculate_levenstein_distance(url_domain)
    print(similarity)
    prediction = ranForest.predict([[similarity]])

    return prediction[0]


def final_prediction(url):
    #prediction_1 = prediction_by_characteristics(url)

    #if blackListCheck:
    #    return True

    #if prediction_1 == 1:
     #   return True
    prediction_2 = prediction_by_similarity(url)

    if prediction_2 == 1:
        print("Phishing")
        return True
    
    return False
    


def groupBlackListCheck(dfURL):
    blackList = pd.read_csv('./datasets/PhishTank-DataSet.csv')
    blackList = pd.DataFrame(blackList)
    blackList = blackList['url']
    banned = False
    blackList['prediction'] = 1  # Esto funciona si quieres asignar una columna "prediction" con valor 1.
    dfPred = pd.merge(dfURL, blackList[['url', 'prediction']], on='url', how='left')
    dfPred.fillna(value=0, inplace=True)


    return dfPred


    







    
    
