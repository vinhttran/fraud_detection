
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

    
#check
def user_unique_events_col():
    user_unique_events = df.groupby('user_created').count().max(axis=1)
    user_unique_events =  pd.DataFrame(user_unique_events,columns=['user_event_count'])
    return df.merge(user_unique_events,how='inner',on='user_created')

#check
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

#check
def convert_date():
    df["approx_payout_date"] = pd.to_datetime(df["approx_payout_date"], unit = 's')
    df["event_created"] = pd.to_datetime(df["event_created"], unit = 's')
    df["event_end"] = pd.to_datetime(df["event_end"], unit = 's')
    df["event_start"] = pd.to_datetime(df["event_start"], unit = 's')
    df["event_published"] = pd.to_datetime(df["event_published"], unit = 's')
    return df

def low_cor_cols(r_score):
    df[num_cols()].corr()[['fraud']].values
    corr_df = df[num_cols()].corr()[['fraud']].sort_values('fraud')
    low_corr_mask = corr_df.sort_values('fraud').abs().lt(r_score).values.reshape(1,-1)[0]
    return corr_df[low_corr_mask]

def get_corrs():
    corr_df = df[num_cols()].corr()[['fraud']].abs().sort_values('fraud')
    return corr_df

def num_cols():
    return df.describe().columns

def drop_cols():
    df1 = df.drop(low_cor_cols(.09).index.tolist(),axis=1)
    df2 = df1.drop(['acct_type','sale_duration','fraud','event_start','approx_payout_date',
                    'event_published','event_end','venue_state',
                    'ticket_types','venue_name','venue_state','venue_country','venue_address',
                    'org_desc','org_name','previous_payouts','email_domain','name','currency','country','event_created'],axis=1)
    return df2

#check
def description_cols():
    import clean_desc
    df['description'] = df['description'].apply(strip_tags)
    clean_desc(df)
    return df

#check
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
    df['publish_time_to_start'] =  df['event_published'] - df['event_created'] 
    df['publish_time_to_start'] = df['publish_time_to_start'].apply(timedelta)
    return df

def has_venue_data():
    df['has_state'] = (df['venue_state'].fillna('None').replace('','None') == 'None').astype(int)
    df['has_country'] = (df['venue_country'].fillna('None').replace('','None') == 'None').astype(int)
    df['has_address'] = (df['venue_address'].fillna('None').replace('','None') == 'None').astype(int)
    df['has_venue_name'] = (df['venue_name'].fillna('None').replace('','None') == 'None').astype(int)
    
    df['has_org_desc'] = (df['org_desc'].fillna('None').replace('','None') == 'None').astype(int)
    df['has_org_name'] = (df['org_name'].fillna('None').replace('','None') == 'None').astype(int)
    df['has_venue_name'] = (df['venue_name'].fillna('None').replace('','None') == 'None').astype(int)
    df['has_venue_name'] = (df['venue_name'].fillna('None').replace('','None') == 'None').astype(int)
    return df

def payout_type():
    df1 = pd.get_dummies(df,columns = ['payout_type','listed'])
    return df1