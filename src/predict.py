from db import DB
import pandas as pd
import numpy as np
import EventAPIClient
from data_preproc import pre_process_data, ticket_types, create_target, prev_pay_count, email_classify, country_classify, isexist, clean_rest

columns_checked = [
    'body_length', 'channels', 'country', 'currency', 'delivery_method',
    'email_domain', 'event_created', 'event_end',
    'event_published', 'event_start', 'fb_published', 'has_analytics',
    'has_header', 'has_logo', 'listed', 'name', 'name_length', 'object_id',
    'org_facebook', 'org_name', 'org_twitter', 'payee_name',
    'payout_type', 'sale_duration', 'sequence_number',
    'show_map', 'user_age', 'user_created', 'user_type',
    'venue_address', 'venue_country', 'venue_latitude', 'venue_longitude',
    'venue_name', 'venue_state', 'predict_proba'
]


class Logic():
    def __init__(self):
        self.db = DB()
        self.event_model, self.user_model, self.event_df = self.db.load_models()

    def predict(self, events):
        '''
    INPUT:
      one event

    OUTPUT:
      risk score from 0: safe to 1: sure fraud
    '''
        # TODO: vectorize the event per event_model
        df = pd.DataFrame(events)
        # print(df.info())

        X = df[['acct_type', 'approx_payout_date', 'body_length', 'channels', 'country',
       'currency', 'delivery_method', 'email_domain', 'event_created',
       'event_end', 'event_published', 'event_start', 'fb_published', 'gts',
       'has_analytics', 'has_header', 'has_logo', 'listed', 'name',
       'name_length', 'num_order', 'num_payouts', 'object_id', 'org_desc',
       'org_facebook', 'org_name', 'org_twitter', 'payee_name', 'payout_type',
       'previous_payouts', 'sale_duration', 'sale_duration2', 'show_map',
       'ticket_types', 'user_age', 'user_created', 'user_type',
       'venue_address', 'venue_country', 'venue_latitude', 'venue_longitude',
       'venue_name', 'venue_state']]

        X=pre_process_data(X)


        # predict
        try:
            predict_proba = self.event_model.predict_proba(X)
            df["predict_proba"] = predict_proba[:,1:2]
        except Exception as e:
            df["predict_proba"] = str(e)

        adding = df.shape[0]

        if isinstance(self.event_df, pd.DataFrame):
            self.event_df.append(df)
        else:
            self.event_df = df

        prev_len = self.event_df.shape[0]
        self.event_df.drop_duplicates(subset=columns_checked, inplace=True) # remove duplicate lines
        self.db.save(self.event_df)

        new_len = self.event_df.shape[0]
        if prev_len == new_len :
          print('New data is duplicate of previous, not adding')
        else:
          delta = new_len - prev_len
          print('Adding {} rows'.format(delta))
          dups = adding - delta 
          if dups > 0:
            print(dups, ' rows were duplicates, not added')

