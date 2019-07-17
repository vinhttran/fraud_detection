import pandas as pd
import pickle

class DB():
    def __init__(self):
        pass

    def load_models(self):
        # TODO: load the models from pickle files
        self.event_model = pickle.load(open('models/baseline_event_model.pkl', 'rb'))
        self.user_model = None#pickle.load(open('models/.pkl', 'rb'))
        self.event_df = pd.DataFrame({'A': None}) # TODO: replace with better template
        return self.event_model, self.user_model, self.event_df

    def set_df(self, df):
        self.df = df

    def save(self):
        # TODO: write dataframe to file
        pickle_out = open("data/event_df.pkl","wb")
