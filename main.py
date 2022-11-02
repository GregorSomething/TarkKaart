# Impordid
import tkinter

import data


# Dokumentatsiooni/ juhiste linkid
# GUI img display https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python

def main():
    print("Start!")
    # Test Data
    cs = data.CardData.CardSide(data.ContentType.TEXT, "Mingi loov tekst")
    c = data.CardData(15, (cs, cs))
    p = "/home/gregor-pc/Downloads/a/"
    cd = data.CardSetData(p, [c, c, c])
    # End of test data


if __name__ == '__main__':
    main()
