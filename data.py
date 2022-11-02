from enum import Enum
import os


class CardData:  # TODO: Kõik vajalikud väljad
    def __init__(self, card_id: int, data: tuple):
        self.card_id: int = card_id
        self.data: tuple[CardData.CardSide, CardData.CardSide] = data

    @staticmethod
    def to_data_string(card) -> str:
        """Meetod, et salvestad CardData stringi.
        :arg card CardData objekt mis muuta stringiks"""
        side1_str, side2_str = map(CardData.CardSide.to_data_string, list(card.data))
        data = "{:0>4d}{:0>4d}{:0>4d}{}{}".format(card.card_id, len(side1_str), len(side1_str), side1_str, side2_str)
        # nii vormistadas, saab hiljem jama edasi kirjutada lihtsamini
        return data

    @staticmethod
    def from_data_string(string: str):
        """Teeb vastupidist vastava to_data_string meetodiga.
        :arg string sisend, mis muuta CardData"""
        str_id = string[:4]
        len_side1 = int(string[4:8])
        len_side2 = int(string[8:12])
        str_side1 = string[12: 12 + len_side1]
        str_side2 = string[12 + len_side1: 12 + len_side1 + len_side2]
        return CardData(int(str_id), tuple(list(map(CardData.CardSide.from_data_string, [str_side1, str_side2]))))

    class CardSide:
        def __init__(self, content_type, content: str):
            self.content_type: ContentType = content_type
            self.content: str = content

        @staticmethod
        def to_data_string(side) -> str:
            """Meetod, et salvestad CardData.CardSide stringi.
            :arg side CardData.CardSide objekt mis muuta stringiks"""
            data = "{}{:0>4d}{}".format(str(side.content_type.value), len(side.content), side.content)
            # nii vormistadas, saab hiljem peale contenti jama edasi kirjutada
            return data

        @staticmethod
        def from_data_string(string: str):
            """Teeb vastupidist vastava to_data_string meetodiga.
            :arg string sisend, mis muuta CardSide"""
            str_type = string[:1]
            len_content = string[1:5]
            content = string[5: 5 + int(len_content)]
            return CardData.CardSide(ContentType.from_value(int(str_type)), content)


class ContentType(Enum):
    NONE = 0
    IMG = 1
    TEXT = 2

    @classmethod
    def from_value(cls, value: int):
        return cls(value)


class CardSetData:  # TODO: Kõik vajalikud väljad
    def __init__(self, data_folder: str, cards: list[CardData]):
        """:arg data_folder kaust kus seti andmed on"""
        self.data_folder: str = data_folder
        self.cards: list[CardData] = cards

    @staticmethod
    def to_data_string(card_set) -> str:
        """Meetod, et salvestad CardSetData stringi.
        :arg card_set CardSetData objekt mis muuta stringiks"""
        data = "{:0>4d}".format(len(card_set.cards))
        for str_card in map(CardData.to_data_string, card_set.cards):
            data += "{:0>4d}{}".format(len(str_card), str_card)
        return data

    @staticmethod
    def from_data_string(string: str, data_folder: str):
        """Teeb vastupidist vastava to_data_string meetodiga.
        :arg string sisend, mis muuta CardSetData
        :arg data_folder andmekaust, kust andmed pärinevad"""
        len_cards = int(string[:4])
        cards: list[CardData] = []
        j = 4  # Viimane koht stringis mida vaadeldi
        for i in range(len_cards):
            len_card = int(string[j:j + 4])
            cards.append(CardData.from_data_string(string[j + 4:j + 4 + len_card]))
            j = j + 4 + len_card
        return CardSetData(data_folder, cards)


class GenericError(Exception):
    def __init__(self, message: str):
        self.message: str = message


def save(path: str, data: CardSetData) -> None:
    cpath: str = os.path.join(path, "data.sav")
    os.makedirs(os.path.join(path, "img"))
    with open(cpath, "w", encoding="UTF-8") as file:
        file.write(CardSetData.to_data_string(data))


def load(path: str) -> CardSetData:
    if not os.listdir(path):
        raise GenericError("Andmekausta puudub.")
    if not os.path.exists(os.path.join(path, "data.sav")):
        raise GenericError("Andmefail puudub.")
    cpath: str = os.path.join(path, "data.sav")
    with open(cpath, "r", encoding="UTF-8") as file:
        return CardSetData.from_data_string("\n".join(file.readlines()).strip(), path) # Read andis vist bin andmeid
