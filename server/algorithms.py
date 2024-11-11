import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import difflib
import tldextract
import Levenshtein
from tqdm import tqdm


def get_MLNB():
    data_set = pd.read_csv('../datasets/DataSet_WebPhishing_Final.csv')

    dfWebPh = pd.DataFrame(data_set)

    feature_cols = ['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash', 'n_questionmark', 'n_equal', 'n_at', 'n_and', 'n_exclamation', 'n_space', 'n_tilde', 'n_comma', 'n_plus', 'n_asterisk', 'n_hastag', 'n_dollar', 'n_percent']
    X = dfWebPh[feature_cols] # Etiquetas
    y = dfWebPh.phishing # Clases

    mlnb = MultinomialNB()

    mlnb.fit(X, y)

    return mlnb

def get_Similarity_Model():
    # Paso 1: Cargar y preparar el dataset
    data = pd.read_csv('../datasets/DataSet_WebPhishing_embedding.csv')

    # Crear características con TF-IDF (basado en caracteres)
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4))
    X = vectorizer.fit_transform(data['Domain'])
    y = data['Phishing']

    # Paso 2: Entrenar el modelo de Isolation Forest para detectar anomalías en URLs legítimas
    legit_X = X[y == 0]  # Solo URLs legítimas
    anomaly_detector = IsolationForest(contamination=0.05, random_state=42)
    anomaly_detector.fit(legit_X)  # Detectar anomalías en URLs legítimas

    # Paso 3: Entrenar el modelo de clasificación con Random Forest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)

    return clf, vectorizer, anomaly_detector

def valueCalc(df):
    valueCalc_df = df[['url']]
    
    valueCalc_df['url_length'] = valueCalc_df['url'].str.len()
    valueCalc_df['n_dots'] = valueCalc_df['url'].str.count('\.')
    valueCalc_df['n_hypens'] = valueCalc_df['url'].str.count('-')
    valueCalc_df['n_underline'] = valueCalc_df['url'].str.count('_')
    valueCalc_df['n_slash'] = valueCalc_df['url'].str.count('/')
    valueCalc_df['n_questionmark'] = valueCalc_df['url'].str.count('\?')
    valueCalc_df['n_equal'] = valueCalc_df['url'].str.count('=')
    valueCalc_df['n_at'] = valueCalc_df['url'].str.count('@')
    valueCalc_df['n_and'] = valueCalc_df['url'].str.count('&')
    valueCalc_df['n_exclamation'] = valueCalc_df['url'].str.count('!')
    valueCalc_df['n_space'] = valueCalc_df['url'].str.count(' ')
    valueCalc_df['n_tilde'] = valueCalc_df['url'].str.count('~')
    valueCalc_df['n_comma'] = valueCalc_df['url'].str.count(',')
    valueCalc_df['n_plus'] =  valueCalc_df['url'].str.count('\+')
    valueCalc_df['n_asterisk'] = valueCalc_df['url'].str.count('\*')
    valueCalc_df['n_hastag'] = valueCalc_df['url'].str.count('#')
    valueCalc_df['n_dollar'] = valueCalc_df['url'].str.count('\$')
    valueCalc_df['n_percent'] = valueCalc_df['url'].str.count('%')
    valueCalc_df['n_hastag'] = valueCalc_df['url'].str.count('#')


    return valueCalc_df

def calculate_levenstein_distance(url):
    legit_domains = pd.read_csv('../datasets/top_websites.csv', delimiter=';')['Domain'].to_list()
    distances = [Levenshtein.distance(url, legit_domain) for legit_domain in legit_domains]
    return min(distances)

def blackListCheck(urlPH):
    blackList = pd.read_csv('../datasets/PhishTank-DataSet.csv')
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

    urlDF.drop('url', axis=1, inplace=True)

    mlnb = get_MLNB()

    prediction = mlnb.predict_proba(urlDF)



    if prediction[0][1] > 0.80:
        return [1]

    return [0]

def prediction_group_by_characteristics(df):
    urlDF = valueCalc(df)

    urlDF = urlDF.drop(columns=['url'])

    mlnb = get_MLNB()

    # Obtener las predicciones de probabilidad para todo el DataFrame
    predictions = mlnb.predict_proba(urlDF)  # Obtener la probabilidad de ser phishing

    # Crear una lista de 1 y 0 basada en la condición de probabilidad
    result = []
    for proba in tqdm(predictions, desc="Procesando características"):
        if proba[1] > 0.80:
            result.append(1)
        else:
            result.append(0)

    return result

def prediction_by_similarity(url):

    domain = get_domain(url)

    clf, vectorizer, anomaly_detector = get_Similarity_Model()

    # Vectorizar la URL
    url_vector = vectorizer.transform([domain])
    
    # Detección de anomalía con Isolation Forest
    is_anomalous = anomaly_detector.predict(url_vector)  # -1 es anómalo, 1 es normal
    
    if is_anomalous == -1:
        return [0]  # URL muy diferente de las legítimas
    
    # Si la URL no es anómala, evaluamos con el clasificador Random Forest
    proba = clf.predict_proba(url_vector)[:, 1]  # Obtener la probabilidad de ser phishing
    if proba[0] > 0.7:
        return [1]
    
    return [0]


def prediction_group_by_similarity(df):
    df_prediction = df[['url']].copy()
    # Extraer los dominios limpios de las URLs
    df_prediction['domain'] = df_prediction['url'].apply(get_domain)

    clf, vectorizer, anomaly_detector = get_Similarity_Model()

    # Vectorizar las URLs
    url_vector = vectorizer.transform(df_prediction['domain'])
    
    # Detección de anomalía con Isolation Forest
    is_anomalous = anomaly_detector.predict(url_vector)  # -1 es anómalo, 1 es normal
    
    # Crear una columna para almacenar los resultados de la predicción
    df_prediction['similarity_prediction'] = 0
    
    # Evaluar con el clasificador Random Forest solo si no es anómalo
    for i in tqdm(range(len(df_prediction)), desc="Procesando similitud"):
        if is_anomalous[i] == -1:
            df_prediction.at[i, 'similarity_prediction'] = 0  # URL muy diferente de las legítimas
        else:
            proba = clf.predict_proba(url_vector[i])[0, 1]  # Obtener la probabilidad de ser phishing
            if proba > 0.7:
                df_prediction.at[i, 'similarity_prediction'] = 1
    print(df_prediction)
    
    return df_prediction[['similarity_prediction']]


def final_prediction(url):

    result = []
    print("URL: ", url)

    if blackListCheck(url):
        print("Blacklist phishing")
        result.append(1)
        result.append("Blacklist phishing")
        return result

    prediction_1 = prediction_by_characteristics(url)
   
    if prediction_1[0] == 1:
        print("Characteristics phishing")
        result.append(1)
        result.append("Characteristics phishing")
        return result

    prediction_2 = prediction_by_similarity(url)
    if prediction_2[0] == 1:
        print("Similarity phishing")
        result.append(1)
        result.append("Similarity phishing")
        return result
    
    return result
    

def group_final_prediction(file):
    # Leer el archivo CSV en un DataFrame
    csvDF = pd.read_csv(file)

    finalDF = csvDF[['url']]
    finalDF['blackList'] = groupBlackListCheck(csvDF[['url']])
    finalDF['characteristic'] = prediction_group_by_characteristics(csvDF[['url']])
    finalDF['similarity'] = prediction_group_by_similarity(csvDF[['url']])
        
    finalDF['prediction'] = finalDF[['blackList', 'characteristic', 'similarity']].any(axis=1).astype(int)

    final_dic = finalDF.to_dict(orient='records')

    return final_dic




def groupBlackListCheck(dfURL):
    # Leer la blacklist
    blackList = pd.read_csv('../datasets/PhishTank-DataSet.csv')
    blackList_urls = blackList['url']

    # Verificar si las URLs están en la blacklist
    dfURL['in_blacklist'] = dfURL['url'].isin(blackList_urls).astype(int)

    # Devolver la lista de 0 y 1
    return dfURL['in_blacklist']
    



    #blackList['prediction'] = 1  # Esto funciona si quieres asignar una columna "prediction" con valor 1.
    #dfPred = pd.merge(dfURL, blackList[['url', 'prediction']], on='url', how='left')
    #dfPred.fillna(value=0, inplace=True)


    return dfPred

    







    
    
