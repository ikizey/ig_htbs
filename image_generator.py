from csv import DictReader

from instaimgcreator import InstaImgCreator


def read_from_csv():
    with open("static/quotes.tsv", 'r') as quotes:
        lines = DictReader(quotes, delimiter='\t', quotechar='"')
        for line in lines:
            if line['post_date'] != '':
                yield line['quote'], line['author']


if __name__ == "__main__":

    FONT_NAME = "DancingScript-SemiBold.ttf"
    SIGNATURE_FONT_NAME = "Brush Script.ttf"
    FONT_SIZE = 140
    SIGNATURE_FONT_NAME
    GREEN_BG_PATH = "static/bg_green.jpeg"
    SIGNATURE_FONT_SIZE = 86

    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(base_dir, 'out')

    iic = InstaImgCreator(
        FONT_NAME, FONT_SIZE, SIGNATURE_FONT_NAME, SIGNATURE_FONT_SIZE, GREEN_BG_PATH,
    )
    for quote, author in read_from_csv():
        iic.text = quote
        iic.signature = author
        iic.imprint_text().imprint_signature().show()  # .bg.save("test.jpeg", "JPEG2000")

        break
