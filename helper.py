import numpy as np 

def fetch_medal_tally(years, country, df):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif years == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country] 
    elif years != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year']== years ] 
    elif years != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year']==years) & (medal_df['region'] == country)]
    if flag == 1 :
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values(by='Year', ascending=True).reset_index()
    else : 
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(by='Gold', ascending=False).reset_index()
    x['Total'] = x.Gold + x.Silver + x.Bronze
    x[['Gold', 'Silver', 'Bronze', 'Total']] = x[['Gold', 'Silver', 'Bronze', 'Total']].astype(int)
    return x 

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values(by='Gold',
                                                                                 ascending=False).reset_index()
    medal_tally['Total'] = medal_tally.Bronze + medal_tally.Gold + medal_tally.Silver
    medal_tally[['Gold', 'Silver', 'Bronze', 'Total']] = medal_tally[['Gold', 'Silver', 'Bronze', 'Total']].astype(int)

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return country, years

def data_over_time(df, col):
    df_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(by='index').\
                        rename(columns= {'index':'Edition', 'Year':col})

    return df_over_time 

def most_successful(df, sport):
    temp_df = df.dropna(subset= ['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport ]
    return temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']]\
         .drop_duplicates('index').rename(columns = {'index':'Name', 'Name_x': 'Medals', 'region':'Region'})

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return temp_df
def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = temp_df[temp_df['region'] == country]
    pt = temp_df.pivot_table(index='Sport', columns= 'Year', values = 'Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset= ['Medal'])
    temp_df = temp_df[temp_df['region'] == country ]
    return temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport']]\
         .drop_duplicates('index').rename(columns = {'index':'Name', 'Name_x': 'Medals'})

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset =['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace =True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset =['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left').rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}).fillna(0).astype(int)
    return final 