import pandas as pd
import pickle
import os

event_file = '../data/streaming_events.xlsx'
sheet_name = 'Streaming Events'

class DB():
    def __init__(self):
        self.pickle_out = open(“pickles/.pkl”,“wb”)

    def load_models(self):
        # TODO: load the models from pickle files
        self.event_model = pickle.load(open('../models/baseline_event_model.pkl', 'rb'))
        self.user_model = None#pickle.load(open('models/.pkl', 'rb'))
        # self.event_df = pd.DataFrame({'A': None}) # TODO: replace with better template
        # if os.path.isfile(event_file):
        #     self.event_df = pd.read_excel(event_file, sheetname=sheet_name)
        # else:
        self.event_df = None
        return self.event_model, self.user_model, self.event_df

    def set_df(self, df):
        self.df = df

    def save(self, df):
        print('Writing new events to Excel!')
        df.to_excel(event_file, sheet_name=sheet_name)
        pickle_out = open(“pickles/tfidf_25kBalancedSamples_20kFeats.pkl”,“wb”)
pickle.dump(tfidf, pickle_out)
pickle_out.close()
