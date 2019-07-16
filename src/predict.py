from db import DB

class Models():
  def __init__(self):
    self.db = DB()
    self.event_model, self.user_model = self.db.load_models()

  def predict(self, event):
    '''
    INPUT:
      one event

    OUTPUT:
      risk score from 0: safe to 1: sure fraud
    '''

    return 0.5  # Basic model!

  def save(self):
    self.db.save()
  