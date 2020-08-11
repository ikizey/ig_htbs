from __future__ import annotations
import csv
import textwrap
from PIL import Image, ImageFont, ImageDraw


FONT_NAME = "DancingScript-SemiBold.ttf"
FONT_SIZE = 140
FONT = ImageFont.truetype(FONT_NAME, FONT_SIZE)

bg_green = Image.open("static/bg_green.jpeg")
# bg_blue = Image.open("static/blue.jpeg")

INNER_BOX_SIZE = (110, 130, 971, 1168)
inner_box = bg_green.crop(INNER_BOX_SIZE)


def fit_text(text: str, image: Image, font: FreeTypeFont) -> str:
    words = text.split(' ')
    lines = [[words.pop(0)]]
    for word in words:
        if font.getsize(' '.join(lines[-1] + [word]))[0] <= image.width:
            lines[-1].append(word)
        else:
            lines += [[word]]
    lines_of_str = [' '.join(line) for line in lines]
    str_of_str = '\n'.join(lines_of_str)
    return str_of_str


def centered_height(image: Image, text: str, font: FreeTypeFont) -> int:
    _, image_height = image.size
    _, text_height = font.getsize_multiline(text)
    centered_height = (image_height / 2 - text_height / 2) / 2
    return centered_height


# font.set_variation_by_name("bold")

with open("static/quotes.tsv", 'r') as quotes:
    lines = csv.DictReader(quotes, delimiter='\t', quotechar='"')
    for line in lines:
        if line['post_date'] != '':
            text = fit_text(line['quote'], inner_box, FONT)
            draw = ImageDraw.Draw(inner_box)
            draw.multiline_text(
                (0, centered_height(inner_box, text, FONT)),
                text,
                fill="black",
                font=FONT,
                spacing=-10,
            )
            inner_box.show()
            bg_green.show()
            break
