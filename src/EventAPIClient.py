import requests
import time
import json
import pandas as pd
from ast import literal_eval


class EventAPIClient:
    """Realtime Events API Client"""

    def __init__(self, first_sequence_number=0,
                 api_url = 'https://hxobin8em5.execute-api.us-west-2.amazonaws.com/api/',
                 api_key = 'vYm9mTUuspeyAWH1v-acfoTlck-tCxwTw9YfCynC',
                 db = None,
                 logic=None):
        """Initialize the API client."""
        self.next_sequence_number = first_sequence_number
        self.api_url = api_url
        self.api_key = api_key
        self.logic = logic

    # def save_to_database(self, row):
    #     """Save a data row to the database."""
    #     # print("Received data:\n")
    #     dico2 = literal_eval(repr(row))
        # print(dico2.keys())

        # OLD
        # print(dico.keys())
        # print(data)
        # little_df = pd.DataFrame(data)
        # print(little_df.info())

    def get_data(self):
        """Fetch data from the API."""
        print('Getting data for sequence', self.next_sequence_number)
        payload = {'api_key': self.api_key,
                   'sequence_number': self.next_sequence_number}
        response = requests.post(self.api_url, json=payload)
        data = response.json()
        self.next_sequence_number = data['_next_sequence_number']
        return data['data']

    def collect(self, interval=30):
        """Check for new data from the API periodically."""
        while True:
            print("Requesting data...")
            data = self.get_data()
            # print(data)
            # print(type(data))
            if data:
                # print("Received data, sending to predict")
                self.logic.predict(data)

                # for row in data:
                #     self.save_to_database(row)
            else:
                print("No new data received.")
            print(f"Waiting {interval} seconds...")
            time.sleep(interval)

if __name__ == "__main__":
    client = EventAPIClient()
    client.collect()