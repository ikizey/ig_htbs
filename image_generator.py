from csv import DictReader
from typing import Generator, List

from PIL import Image, ImageDraw, ImageFont


class InstaImgCreator:
    def __init__(
        self, font_name: str, font_size: int, bg_path: str, text: str = ""
    ) -> None:
        self.font = ImageFont.truetype(font_name, font_size)

        self.bg = Image.open(bg_path)

        # self._inner_box_coords = (110, 130, 971, 1168)
        self.inner_left = 110
        self.inner_right = 971
        self.inner_width = self.inner_right - self.inner_left
        self.inner_top = 130
        self.inner_bottom = 1168
        self.inner_height = self.inner_bottom - self.inner_top

        self._original_text = text
        self.text = self._original_text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = self.list_to_str(self.fit_text(text))

    def get_str_width(self, text: str) -> int:
        """Returns width of text"""
        return self.font.getsize(text)[0]

    def get_str_height(self, text: str) -> int:
        """Returns height of text"""
        return self.font.getsize_multiline(text)[1]

    def fit_text(self, text: str) -> list:
        """Splits the text in lines, so it would fit in the inner box of the image

        Returns list of strings. It gives the ability to use own line spacing.
        """

        words = text.split(" ")

        # TODO DRY
        lines = list()
        line = list()
        for word in words:
            temp_line = line[:]
            temp_line.append(word)
            temp_line_width = self.get_str_width(" ".join(temp_line))
            if temp_line_width > self.inner_width:
                if line:
                    lines.append(" ".join(line))
                    line.clear()
                    line.append(word)
                else:
                    lines.append("".join(temp_line))
                    line.clear()
            else:
                line.append(word)
        if line:
            lines.append(" ".join(line))

        return lines

    def list_to_str(self, lines_of_text: List, sep: str = "\n") -> str:
        """Just combines list of strings to single string"""
        return sep.join(lines_of_text)

    def inner_centered_top(self) -> int:
        """finds vertical coordinate, for text to be vertically centered inside the image"""
        text_height = self.get_str_height(self.text)
        centered = (self.inner_height - text_height) / 2
        return centered

    def imprint_text(self) -> Image.Image:
        """Imprints text to image centered vertically inside inner box
        Returns image
        """
        draw = ImageDraw.Draw(self.bg)
        draw.multiline_text(
            (self.inner_left, self.inner_centered_top()),
            self.text,
            font=self.font,
            fill="black",
            spacing=-10,
        )
        return self.bg


def read_from_csv():
    with open("static/quotes.tsv", 'r') as quotes:
        lines = DictReader(quotes, delimiter='\t', quotechar='"')
        for line in lines:
            if line['post_date'] != '':
                yield line['quote'], line['author']


if __name__ == "__main__":

    FONT_NAME = "DancingScript-SemiBold.ttf"
    FONT_SIZE = 140
    GREEN_BG_PATH = "static/bg_green.jpeg"

    iic = InstaImgCreator(FONT_NAME, FONT_SIZE, GREEN_BG_PATH)
    for quote, author in read_from_csv():
        iic.text = quote
        iic.imprint_text().show()
        break
