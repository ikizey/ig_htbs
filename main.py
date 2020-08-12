from csv import DictReader

from PIL import Image
from PIL import ImageDraw

from utils import MyInstaImgCreator


def read_from_csv():
    with open("static/quotes.tsv", 'r') as quotes:
        lines = DictReader(quotes, delimiter='\t', quotechar='"')
        for line in lines:
            if line['post_date'] != '':
                yield line['quote'], line['author']


if __name__ == "__main__":

    green_bg = Image.open("static/bg_green.jpeg").convert("RGBA")
    blue_bg = Image.open("static/bg_blue.jpeg").convert("RGBA")

    import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(base_dir, 'out')

    iic = MyInstaImgCreator()

    counter = 0
    f_counter = 0
    for quote, author in read_from_csv():
        iic.quote = quote
        iic.author = author

        ## use different backgrounds: 2 green 2 blue
        if counter == 0:
            iic.image = green_bg
        elif counter == 2:
            iic.image = blue_bg
        elif counter > 3:
            counter = -1

        iic.get_complete_image().save(f"out/img{f_counter}.jpeg", "JPEG2000")
        counter += 1
        f_counter += 1
        break
