import pandas as pd
from pandas import DataFrame

data = pd.read_csv(r'C:\Users\deniz\OneDrive\Рабочий стол\Python\datka.csv', na_values = ['*', '**', '***', '****','*****', '******'])

#1 part
#Amount of rows
data_length = len(data)
#Names and datatypes of the columns
data_type = data.dtypes
#Mean temp
Mean = data['TEMP'].mean()
#Sd of max temp
Std = data['MAX'].std()
#Unique stations (USAF)
Unique_values = data['USAF'].unique()

#2 part
selected = data[['USAF', 'YR--MODAHRMN', 'TEMP', 'MAX', 'MIN']]
#remove missing values
selected = selected.dropna(subset=['TEMP'])
#adding temp in Celsuis
selected['Celsuis'] = (selected['TEMP']-32)/1.8
#rounding values in Celsuis
selected['Celsuis'] = selected['Celsuis'].round()
#converting data type into int
selected['Celsuis'] = selected['Celsuis'].astype(int)

#3 part
kumpula = selected.loc[selected.USAF == 29980]
rovaniemi = selected.loc[selected.USAF == 28450]
#exporting data
kumpula.to_csv('Kumpula_temps_May_Aug_2017.csv', sep = ',')
rovaniemi.to_csv('Rovaniemi_temps_May_Aug_2017.csv', sep = ',')

#4 part
Medians = {'kumpula_median': kumpula['Celsuis'].median(), 'rovaniemi_median': rovaniemi['Celsuis'].median()}
#converting to datetime format
kumpula['YR--MODAHRMN'] = pd.to_datetime(kumpula['YR--MODAHRMN'], format = '%Y%m%d%H%M')
rovaniemi['YR--MODAHRMN'] = pd.to_datetime(rovaniemi['YR--MODAHRMN'], format = '%Y%m%d%H%M')
#Changing the name to more convenient one
kumpula.rename(columns = {'YR--MODAHRMN': 'Date'}, inplace = True)
rovaniemi.rename(columns = {'YR--MODAHRMN': 'Date'}, inplace = True)
#Setting date as index
kumpula = kumpula.set_index('Date')
rovaniemi = rovaniemi.set_index('Date')
#Creating new dataframes
kumpula_may = kumpula['2017/05']
kumpula_june = kumpula['2017/06']
rovaniemi_may = rovaniemi['2017/05']
rovaniemi_june = rovaniemi['2017/06']
#Mean, min max of new dataframes
summary = DataFrame({'Mean': [kumpula_may['Celsuis'].mean(), kumpula_june['Celsuis'].mean(), rovaniemi_may['Celsuis'].mean(), rovaniemi_june['Celsuis'].mean()],
                     'Min': [kumpula_may['Celsuis'].min(), kumpula_june['Celsuis'].min(), rovaniemi_may['Celsuis'].min(), rovaniemi_june['Celsuis'].min()],
                     'Max': [kumpula_may['Celsuis'].max(), kumpula_june['Celsuis'].max(), rovaniemi_may['Celsuis'].max(), rovaniemi_june['Celsuis'].max()],
                     'Date':['May', 'June', 'May', 'June']}, index = ['kumpula','kumpula','rovaniemi', 'rovaniemi'])
#Mean, max, min per days
Aggdata = kumpula[['Celsuis']].resample('D').agg({'Mean': 'mean', 'Max': 'max', 'Min': 'min'})
Aggdata['Mean'] = Aggdata['Mean'].round()
Aggdata['Mean'] = Aggdata['Mean'].astype(int)
