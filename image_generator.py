from csv import DictReader
from typing import Generator, List

from PIL import Image, ImageDraw, ImageFont


class InstaImgCreator:
    def __init__(
        self, font_name: str, font_size: int, bg_path: str, text: str = ""
    ) -> None:
        self.font = ImageFont.truetype(font_name, font_size)

        self.bg = Image.open(bg_path)

        self._inner_box_coords = (110, 130, 971, 1168)
        self.inner_left = self._inner_box_coords[0]
        self.inner_width = self._inner_box_coords[2] - self._inner_box_coords[0]
        self.inner_top = self._inner_box_coords[1]
        self.inner_height = self._inner_box_coords[3] - self._inner_box_coords[1]

        self._original_text = text
        self.text = self._original_text
        # self.text = self._original_text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = self.list_to_str(self.fit_text(text))

    def get_str_width(self, text: str) -> int:
        return self.font.getsize(text)[0]

    def get_str_height(self, text: str) -> int:
        return self.font.getsize_multiline(text)[1]

    def fit_text(self, text: str) -> list:
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

    def list_to_str(self, lines_of_text: List) -> str:
        return "\n".join(lines_of_text)

    def centered_top(self) -> int:
        """finds vertical position, to text to be vertically centered"""
        text_height = self.get_str_height(self.text)
        centered = (self.inner_height / 2 - text_height / 2) / 2
        return centered

    def imprint_text(self) -> None:
        draw = ImageDraw.Draw(self.bg)
        draw.multiline_text(
            (self.inner_left, self.centered_top()),
            self.text,
            font=self.font,
            fill="black",
            spacing=-10,
        )


def generate_text_from_csv() -> Generator[str]:
    with open("static/quotes.tsv", 'r') as quotes:
        lines = DictReader(quotes, delimiter='\t', quotechar='"')
        for line in lines:
            if line['post_date'] != '':
                yield line['quote']


if __name__ == "__main__":

    FONT_NAME = "DancingScript-SemiBold.ttf"
    FONT_SIZE = 140
    GREEN_BG_PATH = "static/bg_green.jpeg"

    iic = InstaImgCreator(FONT_NAME, FONT_SIZE, GREEN_BG_PATH)
    for word in generate_text_from_csv():
        iic.text = word
        iic.imprint_text()
        iic.bg.show()
        break
