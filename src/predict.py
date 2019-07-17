from db import DB

class Logic():
  def __init__(self):
    self.db = DB()
    self.event_model, self.user_model, self.event_df = self.db.load_models()

  def predict(self, json_event):
    '''
    INPUT:
      one event

    OUTPUT:
      risk score from 0: safe to 1: sure fraud
    '''
    # TODO: vectorize the event per event_model

    # predict 

    # TODO: add the data + score as 1 row in the event_df

    return 0.5  # Basic model!

  def save(self):
    self.db.save()
  