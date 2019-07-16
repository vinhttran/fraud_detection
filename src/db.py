import pandas as pd

class DB():
    def __init__(self):
        self.events = pd.DataFrame({'A': None}) # TODO: replace with better template

    def load_models(self):
        # TODO: load the models from pickle files
        event_model = pickle.load(open('models/baseline_event_model.pkl', 'rb'))
        user_model = None#pickle.load(open('models/.pkl', 'rb'))
        return event_model, user_model

    def save(self):
        # TODO: write dataframe to file
        pass
