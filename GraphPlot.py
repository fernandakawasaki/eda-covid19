import pandas as pd
from matplotlib import pyplot as plt
PATH = '/content/drive/My Drive/Iniciacao Cientifica'

def top_cases(df_pr, df_confirmed, MAX): #get all data from the top 10 cities with most confirmed cases
    df_full_confirmed = pd.DataFrame()
    cities_confirmed = df_confirmed["city"].tolist() #top10 confirmed cities list
    for city in cities_confirmed:
        df_full_confirmed = df_full_confirmed.append(df_pr[df_pr['city'].str.match(city)]) #df with data from the top10 confirmed cities
    return df_full_confirmed #dataframe containing all the records for each city with most confirmed cases

def top_deaths(df_pr, df_deaths, MAX): #get all data from the top 10 cities with most confirmed cases
    df_full_deaths = pd.DataFrame()
    cities_deaths = df_deaths["city"].tolist() #top10 deaths cities list
    for city in cities_deaths:
        df_full_deaths = df_full_deaths.append(df_pr[df_pr['city'].str.match(city)]) #df with data from the top10 death cities
    return df_full_deaths #dataframe containing all the records for each city with most deaths

def plot_total_confirmed(df_full_confirmed): #plot graph "Date x number of confirmed cases (total)" for the top 10 cities with confirmed cases
    df_total_confirmed = df_full_confirmed.pivot(index='date', columns='city', values='last_available_confirmed') #produce pivot table
    df_total_confirmed.plot(figsize=(16,10)) #define size of the image
    #elements of the graph
    plt.xlabel('Data')
    plt.ylabel('Número de casos (total)')
    plt.legend(title="Cidades")
    plt.title('Casos confirmados de COVID-19')
    #save the result to google drive
    plt.savefig(f"{PATH}/graphs/date_total_cases.png")

def plot_total_deaths(df_full_deaths): #plot graph "Date x number of deaths (total)" for the top 10 cities with deaths
    df_total_deaths = df_full_deaths.pivot(index='date', columns='city', values='last_available_deaths') #produce pivot table
    df_total_deaths.plot(figsize=(16,10)) #define size of the image
    #elements of the graph
    plt.xlabel('Data')
    plt.ylabel('Número de mortes (total)')
    plt.legend(title="Cidades")
    plt.title('Mortes por COVID-19')
    #save the result to google drive
    plt.savefig(f"{PATH}/graphs/date_total_deaths.png")

def plot_confirmed_day(df_full_confirmed): #plot graph "Date x number of confirmed cases (per day)" for the top 10 cities with confirmed cases
    df_daily_confirmed = df_full_confirmed.pivot(index='date', columns='city', values='new_confirmed') #produce pivot table
    df_daily_confirmed.plot(figsize=(16,10)) #define size of the image
    #elements of the graph
    plt.xlabel('Data')
    plt.ylabel('Número de casos (por dia)')
    plt.legend(title="Cidades")
    plt.title('Casos confirmados de COVID-19')
    #save the result to google drive
    plt.savefig(f"{PATH}/graphs/date_day_cases.png")

def plot_deaths_day(df_full_deaths): #plot graph "Date x number of deaths (per day)" for the top 10 cities with deaths
    df_daily_deaths = df_full_deaths.pivot(index='date', columns='city', values='new_deaths') #produce pivot table
    df_daily_deaths.plot(figsize=(16,10)) #define size of the image
    #elements of the graph
    plt.xlabel('Data')
    plt.ylabel('Número de mortes (por dia)')
    plt.legend(title="Cidades")
    plt.title('Mortes por COVID-19')
    #save the result to google drive
    plt.savefig(f"{PATH}/graphs/date_day_deaths.png")

def plot_deaths_week(df_full_deaths): #plot graph "Date x number of deaths (weekly)" for the top 10 cities with deaths (because daily deaths usually does not have a lot of entries)
    df_weekly_deaths = df_full_deaths[['city', 'date', 'new_deaths']].copy(deep=True) #create new dataframe based on columns of df_full_deaths
    df_weekly_deaths['date'] = pd.to_datetime(df_weekly_deaths['date']) #change type of 'date' column to datetime
    df_weekly_deaths = df_weekly_deaths.groupby(['city', pd.Grouper(key='date', freq='W')])['new_deaths'].sum().reset_index() #group days into weeks
    df_weekly_deaths['date'] = df_weekly_deaths['date'].dt.date
    df_weekly_deaths = df_weekly_deaths.pivot(index='date', columns='city', values='new_deaths') #produce pivot table

    #plot graph
    df_weekly_deaths.plot.bar(figsize=(16,10)) #define size of the image
    #elements of the graph
    plt.xlabel('Data')
    plt.ylabel('Número de mortes (por semana)')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title="Cidades")
    plt.title('Mortes por COVID-19')
    #save the result to google drive
    plt.savefig(f"{PATH}/graphs/date_week_deaths.png")

def plot_tm_confirmed(df_full_confirmed, df_confirmed): #plot graph "cities x mean and number of confirmed cases (total)"
    count_confirmed = df_full_confirmed['city'].value_counts() #number of days with covid-19 for each city
    count_confirmed = count_confirmed.to_frame().reset_index().rename(columns={'city': 'num_days', 'index': 'city'}) #change index and columns names
    df_confirmed = df_confirmed.merge(count_confirmed, on='city') #merge number of days into df column
    df_confirmed['mean'] = df_confirmed['last_available_confirmed']/df_confirmed['num_days'] #calculate mean
    df_confirmed = df_confirmed.pivot_table(index="city", values="mean") #produce pivot table

    #plot graph
    df_confirmed.plot.bar(figsize=(16,10), legend=None) #define size of the image
    plt.gcf().subplots_adjust(bottom=0.25)
    #elements of the graph
    plt.xlabel('Média diária')
    plt.ylabel('Número de casos')
    plt.xticks(rotation=45, ha='right')
    plt.title('Gráfico Cidades x Casos Confirmados de COVID-19 (Média diária)')
    #save the result to google drive
    plt.savefig(f"{PATH}/graphs/date_tm_cases.png")

def plot_tm_deaths(df_full_deaths, df_deaths): #plot graph "cities x mean and number of deaths (total)"
    count_deaths = df_full_deaths['city'].value_counts() #number of days with covid-19 for each city
    count_deaths = count_deaths.to_frame().reset_index().rename(columns={'city': 'num_days', 'index': 'city'}) #change index and columns names
    df_deaths = df_deaths.merge(count_deaths, on='city') #merge number of days into df column
    df_deaths['mean'] = df_deaths['last_available_deaths']/df_deaths['num_days'] #calculate mean
    df_deaths = df_deaths.pivot_table(index="city", values="mean") #produce pivot table

    #plot graph
    df_deaths.plot.bar(figsize=(16,10), legend=None) #define size of the image
    plt.gcf().subplots_adjust(bottom=0.25)
    #elements of the graph
    plt.xlabel('Média diária')
    plt.ylabel('Número de mortes')
    plt.xticks(rotation=45, ha='right')
    plt.title('Gráfico Cidades x Mortes por COVID-19 (Média diária)')
    #save the result to google drive
    plt.savefig(f"{PATH}/graphs/date_tm_deaths.png")