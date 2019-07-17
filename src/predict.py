from db import DB
import pandas as pd
import EventAPIClient

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

        X = df[["user_type", "user_age", "channels", "name_length"]]

        # predict
        try:
            predict_proba = self.event_model.predict_proba(X)
            df["predict_proba"] = predict_proba[:,1:2]
        except Exception as e:
            df["predict_proba"] = str(e)

        if isinstance(self.event_df, pd.DataFrame):
            self.event_df.append(df)
        else:
            self.event_df = df

        self.event_df.drop_duplicates(subset=columns_checked, inplace=True) # remove duplicate lines
        self.db.save(self.event_df)
