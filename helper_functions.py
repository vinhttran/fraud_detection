import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 500)

import seaborn as sns
import nltk
nltk.download('words')
pd.set_option('max_colwidth', 40)
import os
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
sws = set(stopwords.words('english'))
punctuation = set(string.punctuation)

def user_event_count():
    df['user_event_count'] = df.groupby('user_created').count().max(axis=1)
    return df

def previous_payouts(df):
    new_df=pd.DataFrame(df.previous_payouts[0])
    for i in range(1,df.previous_payouts.shape[0]):
        df_element=pd.DataFrame(df.previous_payouts[i])
        new_df=pd.concat([new_df, df_element])
    return new_df

def user_df():
    unique_cols = []
    for col in columns:
        if unique_col_indicator(df,col):
            unique_cols.append(col)
    user_unique_events = df.groupby('user_created').count().max(axis=1)
    user_unique_events = pd.DataFrame(user_unique_events,columns=['user_event_count'])
    return df[unique_cols].merge(user_unique_events,how='inner',on='user_created')

def unique_col_indicator(df,col):
    try:
        col_count = df.groupby(['user_created',col])['channels'].count().shape[0]
        user_count = df.groupby(['user_created'])['channels'].count().shape[0]
        if col_count == user_count:
            return True
        else:

            return False
    except:
        pass

def user_unique_events_col():
    user_unique_events = df.groupby('user_created').count().max(axis=1)
    user_unique_events =  pd.DataFrame(user_unique_events,columns=['user_event_count'])
    return df.merge(user_unique_events,how='inner',on='user_created')

def create_target():
    df['fraud'] = df['acct_type'].map({'fraudster_event': 1,
                                   'premium': 0,
                                   'spammer_warn': 0,
                                   'fraudster': 1,
                                   'spammer_limited': 0,
                                   'spammer_noinvite': 0,
                                   'locked': 1,
                                   'tos_lock': 0,
                                   'tos_warn': 0,
                                   'fraudster_att': 1,
                                   'spammer_web': 0,
                                   'spammer': 0})
    return df

from datetime import datetime
def convert_date():
    df["approx_payout_date"] = pd.to_datetime(df["approx_payout_date"], unit = 's')
    df["event_created"] = pd.to_datetime(df["event_created"], unit = 's')
    df["event_end"] = pd.to_datetime(df["event_end"], unit = 's')
    df["event_start"] = pd.to_datetime(df["event_start"], unit = 's')
    return df

def low_cor_cols(r_score):
    df[num_columns].corr()[['fraud']].values
    corr_df = df[num_columns].corr()[['fraud']].sort_values('fraud')
    low_corr_mask = corr_df.sort_values('fraud').abs().lt(r_score).values.reshape(1,-1)[0]
    return corr_df[low_corr_mask]

def drop_cols():
    df.drop(['acct_type'],axis=1)
    return df

def description_cols():
    import clean_desc
    df['description'] = df['description'].apply(strip_tags)
    clean_desc(df)
    return df

def ticket_types(df):
    new_df=pd.DataFrame(df.ticket_types[0])
    result_df=new_df[['quantity_sold', 'quantity_total', 'event_id']].groupby('event_id').sum()
    result_df=result_df.join(new_df[['availability', 'cost', 'event_id']].groupby('event_id').mean())

    for i in range(1,df.shape[0]):
        try:
            df_element=pd.DataFrame(df.ticket_types[i])
            grp_ele_df=df_element[['quantity_sold', 'quantity_total', 'event_id']].groupby('event_id').sum()
            grp_ele_df=grp_ele_df.join(df_element[['availability', 'cost', 'event_id']].groupby('event_id').mean())
            result_df=pd.concat([result_df, grp_ele_df])

        except:
            continue
    result_df.reset_index(inplace=True)
    result_df.columns=['object_id', 'quantity_sold', 'quantity_total', 'availability', 'cost']
    final_df=df.set_index('object_id').join(result_df.set_index('object_id'))
    final_df.reset_index(inplace=True)
    final_df[['quantity_sold', 'quantity_total','availability', 'cost']]=final_df[['quantity_sold', 'quantity_total','availability', 'cost']].fillna(0)
    return final_df

def timedelta(field):
    return field.days

def event_times():
    df['event_duration'] = df['event_end'] - df['event_created'] 
    df['publish_time_to_start'] =  df['event_published'] - df['event_created'] 
    return df


def has_venue_data():
    df['has_state'] = (df['venue_state'].fillna('None').replace('','None') == 'None').astype(int)
    df['has_country'] = (df['venue_country'].fillna('None').replace('','None') == 'None').astype(int)
    df['has_address'] = (df['venue_address'].fillna('None').replace('','None') == 'None').astype(int)
    df['has_venue_name'] = (df['venue_name'].fillna('None').replace('','None') == 'None').astype(int)
    return df