from typing import Callable
import cv2

from data import CardSetData, CardData


def get_image_processor(max_x: int, max_y: int, set_data: CardSetData) -> Callable[[str, CardData], tuple[bool, str]]:
    """ Teeb töötlus funktsiooni
    :arg max_x Maksimaalne laius
    :arg max_y Maksimaalne kõrgus
    :arg set_data Set kuhu pilt kuulub"""

    def img_proc(path_from: str, img_id: str) -> tuple[bool, str]:
        img = cv2.imread(path_from)  # Loeb pildi
        cy, cx, _ = img.shape  # Võtab hetke suuruse suuruse
        if cx > cy:
            # Kui x on suurem, kui y siis suurendab soovituks selle järgi,
            # Kui pilt on hekel väiksem soovitud max x siis suurendab, muidu vöhendab
            cv2.resize(img, None, fx=(max_x / cx), fy=(max_x / cx))
        else:
            img = cv2.resize(img, None, fx=(max_y / cy), fy=(max_y / cy))
        # Salvestab pildi asukohta nimega
        cv2.imwrite(f"{set_data.data_folder}img/{img_id}.ppm", img) # GUI vajab .ppm formaati
        return True, "Ok"

    return img_proc
