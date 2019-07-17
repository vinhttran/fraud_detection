import requests
import time

class API2():
  def __init__(self, logic):
    self.url = 'http://galvanize-case-study-on-fraud.herokuapp.com/data_point'
    self.logic = logic

  def collect(self, interval=10):
        """Check for new data from the API periodically."""
        while True:
            print("Requesting data...")
            response = requests.get(self.url)
            raw_data = response.json()

            if raw_data:
                # print("Received data, sending to predict")
                self.logic.predict(raw_data)

                # for row in data:
                #     self.save_to_database(row)
            else:
                print("No new data received.")

            print(f"Waiting {interval} seconds...")
            time.sleep(interval)


