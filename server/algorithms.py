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
    data_set = pd.read_csv('../datasets/DataSet_WebPhishing_Final.csv')

    dfWebPh = pd.DataFrame(data_set)

    #Separo DataSet en Etiquetas y columna de Clases (0 good / 1 bad)
    feature_cols = ['url_length', 'n_dots', 'n_hypens', 'n_underline', 'n_slash', 'n_questionmark', 'n_equal', 'n_at', 'n_and', 'n_exclamation', 'n_space', 'n_tilde', 'n_comma', 'n_plus', 'n_asterisk', 'n_hastag', 'n_dollar', 'n_percent']
    X = dfWebPh[feature_cols] # Etiquetas
    y = dfWebPh.phishing # Clases

    mlnb = MultinomialNB()

    mlnb.fit(X, y)

    return mlnb

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

    urlDF = urlDF.drop(columns=['url'])

    mlnb = get_MLNB()

    prediction = mlnb.predict(urlDF)

    return prediction

def prediction_group_by_characteristics(df):
    urlDF = valueCalc(df)

    urlDF = urlDF.drop(columns=['url'])
    print(urlDF.head())

    mlnb = get_MLNB()

    prediction = mlnb.predict(urlDF)

    print(prediction)

    return prediction

def prediction_by_similarity(url):
    url_domain = get_domain(url)
    print(url_domain)
    ranForest = get_Similarity_Model()
    similarity = calculate_levenstein_distance(url_domain)
    prediction = ranForest.predict([[similarity]])

    return prediction

def prediction_group_by_similarity(df):
    df_prediction = df[['url']]
    # Extraer los dominios limpios de las URLs
    df_prediction['domain'] = df_prediction['url'].apply(get_domain)
    
    # Calcular la distancia de Levenshtein para cada dominio
    df_prediction['similarity'] = df_prediction['domain'].apply(calculate_levenstein_distance)
    print(df_prediction.head())
    
    # Obtener el modelo de Random Forest
    ranForest = get_Similarity_Model()
    similarity_list = df_prediction['similarity'].values.reshape(-1, 1)
    prediction = ranForest.predict(similarity_list)
    print(prediction)

    return prediction


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

    # Extraer la columna de URLs (suponiendo que la columna se llama 'url')
    df_urlPredict = csvDF[['url']]
 
    
    # Calcular las características de las URLs
    df_urlPredict = valueCalc(df_urlPredict)

    finalDF = csvDF[['url']]
    finalDF['blackList'] = groupBlackListCheck(csvDF[['url']])
    finalDF['characteristic'] = prediction_group_by_characteristics(csvDF[['url']])
    print(finalDF.head())
    finalDF['similarity'] = prediction_group_by_similarity(csvDF[['url']])





    # finalDF = csvDF[['url']]
    # finalDF['prediction'] = prediction
    # finalDF['finalPrediction'] = complementaryPrediction(finalDF['url'], finalDF['prediction'])       

    # # Contar las predicciones y crear el resultado
    # prediction_counts = pd.Series(finalDF['finalPrediction']).value_counts().to_dict()



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

    







    
    
