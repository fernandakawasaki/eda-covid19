import pandas as pd
from re import search #regular expressions

def remove_parentheses(city_name): #Function to remove parentheses
    if search('\(.*', city_name): #Search for opening brackets with values inside
        pos = search(' \(.*', city_name).start() #Extract the position of the beginning of the pattern
        return city_name[:pos] #Return the cleaned name
    else:
        return city_name

def clean_airports_df(file_airports):
    df_airports = pd.read_csv(file_airports, skiprows=3)
    df_airports['airports'] = True #create a column with True in every row
    df_airports = pd.concat([df_airports['MUNICÍPIO'], df_airports['airports']], axis=1) #only get the necessary columns
    df_airports = df_airports.drop(df_airports.index[0:2]) #remove extra rows
    df_airports.reset_index(drop=True, inplace=True)
    df_airports = df_airports.replace(to_replace ='\n', value = ' ', regex = True)
    df_airports['MUNICÍPIO'] = df_airports['MUNICÍPIO'].apply(remove_parentheses) #Update the city columns
    return df_airports

def add_airports(df_airports, newest_df):
    df_airports['lower_city'] = df_airports['MUNICÍPIO'].str.lower()
    df_airports = df_airports.drop('MUNICÍPIO', axis=1)
    newest_df['lower_city'] = newest_df['city'].str.lower()

    if 'airports' in newest_df.columns:
        newest_df.drop('airports', axis=1, inplace=True)
    newest_df = newest_df.merge(df_airports, on='lower_city', how='outer')
    newest_df = newest_df.drop('lower_city', axis=1)
    newest_df['airports'].fillna(value=False, inplace=True)
    return newest_df
