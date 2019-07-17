import pandas as pd
import pickle
import os

event_file = '../data/streaming_events.xlsx'
event_pickle = '../db/new_events.pkl'
sheet_name = 'Streaming Events'

class DB():
    def __init__(self):
        pass

    def load_models(self):
        # TODO: load the models from pickle files
        self.event_model = pickle.load(
            open('../models/RF_event_model.pkl', 'rb'))
        self.user_model = None#pickle.load(open('models/.pkl', 'rb'))
        # self.event_df = pd.DataFrame({'A': None}) # TODO: replace with better template
        if os.path.isfile(event_pickle):
            # self.event_df = pd.read_excel(event_file, sheetname=sheet_name)
            print('Loading older events')
            pickle_in = open(event_pickle,'rb')
            self.event_df = pickle.load(pickle_in)
        else:
            print('NOT loading older events')
            self.event_df = None
        return self.event_model, self.user_model, self.event_df

    def set_df(self, df):
        self.df = df

    def save(self, df):
        print('Writing {} new events to Excel and pickle!'.format(len(df.index)))

        df.to_excel(event_file, sheet_name=sheet_name)
        pickle_out = open(event_pickle,'wb')
        pickle.dump(df, pickle_out)
        pickle_out.close()
