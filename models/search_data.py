from models.betting_data import BettingData
from models.user_data import UserData

class SearchData:
    def __init__(self, bet_data:BettingData, user_data:UserData):
        self._bet_data = bet_data
        self._user_data = user_data

    @property
    def data(self):
        return {
            **self._user_data.data, # returning the dict returned by UserData class
            'data': self._bet_data.data
        }