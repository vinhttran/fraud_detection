from db import DB
import EventAPIClient


class Logic():
    def __init__(self):
        self.db = DB()
        self.event_model, self.user_model, self.event_df = self.db.load_models()

    def predict(self, event_dict):
        '''
    INPUT:
      one event

    OUTPUT:
      risk score from 0: safe to 1: sure fraud
    '''
        # TODO: vectorize the event per event_model
        df = pd.DataFrame.from_dict(event_dict)
        X = df[["user_type", "user_age", "channels", "name_length"]]

        # predict
        X["predict_proba"] = self.event_model.predict_proba(X)

        # TODO: add the data + score as 1 row in the event_df
        self.event_df.append(x)
        self.event_df.drop_duplicates(inplace=True) # remove duplicate lines
        self.db.save()
