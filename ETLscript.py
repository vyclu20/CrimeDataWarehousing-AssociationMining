import pandas as pd

#overall csv related. i purposely made separate functions for my convenience, incase i needed to restart something
def allcsv():
    #removes unenriched rows from og crime file, then combines the rest of the file
    df = pd.read_csv('crime.csv', header=None)
    #rows up to 25470
    index_to_remove = df[df[0] == 25470].index[0]
    df = df.drop(df.index[index_to_remove+1:])
    df.to_csv('crime.csv', index=False, header=None)

    df1 = pd.read_csv('crime.csv')
    df2 = pd.read_csv('crime_25471_50000.csv')
    df3 = pd.read_csv('crime_50001_75000.csv')
    df4 = pd.read_csv('crime_75001_100000.csv')
    df5 = pd.read_csv('crime_100001_125000.csv')
    df6 = pd.read_csv('crime_125001_150000.csv')
    df7 = pd.read_csv('crime_150001_175000.csv')
    df8 = pd.read_csv('crime_175001_200000.csv')
    df9 = pd.read_csv('crime_200001_225000.csv')

    combined_df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9], axis=0)

    #drop the last two columns, bc it generated some extra stuff 
    combined_df = combined_df.iloc[:, :-1]
    #renamed header for convenience
    combined_df = combined_df.rename(columns={'Unnamed: 0': 'id'})
    
    combined_df.to_csv('crime.csv', index=False)

def replace_neighborhood():
    df = pd.read_csv("crime.csv", dtype=str)

    #replace empty neighborhood values with values from neighborhood_lookup
    for i in range(len(df)):
        if pd.isna(df.at[i, 'neighborhood']):
            df.at[i, 'neighborhood'] = df.at[i, 'neighbourhood_lookup']

    df.to_csv("crime.csv", index=False)

def removecols():
    df = pd.read_csv("crime.csv")

    #fill missing values in 'country' column with 'United States'
    df['country'].fillna('United States', inplace=True)

    #drop rows with empty cells in said columns
    columns_to_check = ['crime','date','neighborhood','npu','road','county','city','state','country']
    df.dropna(subset=columns_to_check, inplace=True)

    #select the columns to save
    cols_to_save = ['id'] + columns_to_check
    df.loc[:, cols_to_save].to_csv("crime.csv", index=False)

def removeduplicates():
    df = pd.read_csv("crime.csv")
    df.drop_duplicates(subset=df.columns.difference(['id']), inplace=True)
    df.to_csv("crime.csv", index=False)

#stopping at this part, i decided to manually clean some rows I didn't need on excel
#like for example, I had one row of Sandy Springs for city, and that value is insignificant. or fixing spelling errors, like 17th St NW (northwest)
#ran the remove duplicates function one more time after this
#this is where the dim and fact table stuff starts, using the already cleaned data

#crime related
def crimedim():
    df = pd.read_csv("crime.csv")

    crime_severity = {
        'HOMICIDE': 0,
        'RAPE': 1,
        'AGG ASSAULT': 2,
        'ROBBERY-PEDESTRIAN': 3,
        'ROBBERY-RESIDENCE': 4,
        'ROBBERY-COMMERCIAL': 6,
        'BURGLARY-RESIDENCE': 7,
        'BURGLARY-NONRES': 8,
        'AUTO THEFT': 9,
        'LARCENY-FROM VEHICLE': 10,
        'LARCENY-NON VEHICLE': 11
    }

    df_severity = df[['id', 'crime']].copy()
    #map the crime severity values to the 'crime' column
    df_severity['crime_severity'] = df_severity['crime'].map(crime_severity)
    #drop invalid rows
    df_severity.dropna(subset=['crime_severity'], inplace=True)
    df_severity.to_csv("crimeIDS.csv", index=False)
    #drops duplicates
    no_duplicates('crimeIDS.csv', 'dimcrime.csv')


def crimeid():
    #for fact table, crime_key
    dimcrime1 = pd.read_csv('dimcrime.csv')
    crimedim = pd.read_csv('crimeIDS.csv')

    key_map = dict(zip(dimcrime1[['crime', 'crime_severity']].apply(tuple, axis=1), dimcrime1['key']))
    crimedim['id'] = crimedim[['crime', 'crime_severity']].apply(tuple, axis=1).map(key_map)

    crimedim.to_csv('crimeIDS.csv', index=False)

#date related
def datedim():
    df = pd.read_csv('crime.csv', usecols=['id', 'date'])

    #extract year, month, and day from the date column
    df['year'] = pd.DatetimeIndex(df['date']).year

    #extract year quarter
    df['year quarter'] = pd.PeriodIndex(pd.to_datetime(df['date']), freq='Q').strftime('%qQ%y')
    df['year quarter'] = df['year quarter'].str[:-3] + 'Q'

    df['month'] = pd.DatetimeIndex(df['date']).month

    #map the month numbers to month names
    month_names = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
    df['month'] = df['month'].map(month_names)

    df['day'] = pd.DatetimeIndex(df['date']).day
    #extract day of the week
    df['day of the week'] = pd.DatetimeIndex(df['date']).day_name()

    #map day of the week to weekday/weekend
    weekend_days = ['Saturday', 'Sunday']
    df['weekday/weekend'] = df['day of the week'].apply(lambda x: 'weekend' if x in weekend_days else 'weekday')

    df.to_csv('dateIDS.csv', index=False)
    no_duplicates('dateIDS.csv', 'dimdate.csv')

def dateid():
    #for fact table, date_key
    dimdate1 = pd.read_csv('dimdate.csv')
    datedim = pd.read_csv('dateIDS.csv')

    key_map = dict(zip(dimdate1[['date', 'year','year quarter','month','day','day of the week','weekday/weekend']].apply(tuple, axis=1), dimdate1['key']))
    datedim['id'] = datedim[['date', 'year','year quarter','month','day','day of the week','weekday/weekend']].apply(tuple, axis=1).map(key_map)

    datedim.to_csv('dateIDS.csv', index=False)

#loc1 related
def loc1dim():
    df = pd.read_csv('crime.csv', usecols=['id', 'neighborhood', 'npu'])
    df.to_csv('loc1IDS.csv', index=False)
    no_duplicates('loc1IDS.csv', 'dimloc1.csv')

def loc1id():
    #for fact table, loc1_key
    dimloc11 = pd.read_csv('dimloc1.csv')
    loc1dim = pd.read_csv('loc1IDS.csv')

    key_map = dict(zip(dimloc11[['neighborhood','npu']].apply(tuple, axis=1), dimloc11['key']))
    loc1dim['id'] = loc1dim[['neighborhood','npu']].apply(tuple, axis=1).map(key_map)

    loc1dim.to_csv('loc1IDS.csv', index=False)

#loc2 related
def loc2dim():
    df = pd.read_csv('crime.csv', usecols=['id', 'country','state','city','county','road'])
    df.to_csv('loc2IDS.csv', index=False)
    no_duplicates('loc2IDS.csv', 'dimloc2.csv')

def loc2id():
    #for fact table, loc2_key
    dimloc21 = pd.read_csv('dimloc2.csv')
    loc2dim = pd.read_csv('loc2IDS.csv')

    key_map = dict(zip(dimloc21[['country','state','city','county','road']].apply(tuple, axis=1), dimloc21['key']))
    loc2dim['id'] = loc2dim[['country','state','city','county','road']].apply(tuple, axis=1).map(key_map)

    loc2dim.to_csv('loc2IDS.csv', index=False)

def fact():
    df = pd.read_csv('crime.csv', usecols=['id'])
    df = pd.concat([df, pd.read_csv('crimeIDS.csv', usecols=['id']).rename(columns={'id': 'crimekey'})], axis=1)
    df = pd.concat([df, pd.read_csv('dateIDS.csv', usecols=['id']).rename(columns={'id': 'datekey'})], axis=1)
    df = pd.concat([df, pd.read_csv('loc1IDS.csv', usecols=['id']).rename(columns={'id': 'loc1key'})], axis=1)
    df = pd.concat([df, pd.read_csv('loc2IDS.csv', usecols=['id']).rename(columns={'id': 'loc2key'})], axis=1)

    #add a count column with 1's
    count = [1]*len(df)
    df['countn'] = count
    df.to_csv('fact.csv', index=False, float_format='%.0f', sep=',')

#extra functions
def no_duplicates(input_file, output_file):
    #removes all duplicates, with parameters
    df = pd.read_csv(input_file)
    df.drop_duplicates(subset=df.columns.difference(['id']), inplace=True)
    #reset index
    df.reset_index(drop=True, inplace=True)
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'key'}, inplace=True)
    df.drop('id', axis=1, inplace=True)
    
    df.to_csv(output_file, index=False)

def colshift():
    #reordering columns
    df = pd.read_csv('dimloc1.csv')
    df1 = pd.read_csv('dimloc2.csv')
    df2 = pd.read_csv('dimdate.csv')

    df = df[['key','npu','neighborhood']]
    df1 = df1[['key','country','state','city','county','road']]
    df2 = df2[['key','year','year quarter','month','weekday/weekend','day of the week','date','day']]

    # Save the updated dataframe to a new CSV file
    df.to_csv('dimloc1.csv', index=False)
    df1.to_csv('dimloc2.csv', index=False)
    df2.to_csv('dimdate.csv', index=False)

#uncomment to run (ctrl /)
# allcsv()
# replace_neighborhood()
# removecols()
# removeduplicates()
# crimedim()
# crimeid()
# datedim()
# dateid()
# loc1dim()
# loc1id()
# loc2dim()
# loc2id()
# fact()
# colshift()

