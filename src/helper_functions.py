def user_event_count():
    df['user_event_count'] = df.groupby('user_created').count().max(axis=1)
    return df

def ticket_types(df):
    new_df=pd.DataFrame(df.ticket_types[0])
    for i in range(1,df.ticket_types.shape[0]):
        df_element=pd.DataFrame(df.ticket_types[i])
        new_df=pd.concat([new_df, df_element])
    return new_df

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
