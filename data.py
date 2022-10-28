class CardData:  # TODO: Kõik vajalikud väljad
    def __init__(self, card_id: str):
        self.card_id: str = card_id


class CardSetData:  # TODO: Kõik vajalikud väljad
    def __init__(self, data_folder: str):
        """:arg data_folder kaust kus seti andmed on"""
        self.data_folder: str = data_folder
