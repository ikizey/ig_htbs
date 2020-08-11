from csv import DictReader

from PIL import Image, ImageDraw, ImageFont


class InstaImgCreator:
    def __init__(
        self,
        font_name: str,
        font_size: int,
        bg_path: str,
        text: str = "",
        signature: str = "",
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

        self.signature = signature
        self.text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = self.text_wrap(text)  # self.list_to_str(self.fit_text(text))

    @property
    def signature(self) -> str:
        return self._signature

    @signature.setter
    def signature(self, text: str) -> None:
        self._signature = text if text.startswith("-") else f"-{text}"

    def get_str_width(self, text: str) -> int:
        """Returns width of text"""
        return self.font.getsize(text)[0]

    def get_str_height(self, text: str) -> int:
        """Returns height of text"""
        return self.font.getsize_multiline(text)[1]

    def fit_inner(self, text: str) -> bool:
        """Checks if text fits into inner box"""
        return self.get_str_width(text) <= self.inner_width

    def text_wrap(self, text: str) -> str:
        """Wraps text, so it would fit in the inner box"""

        chars = list(text)
        left_cursor = 0
        prevous_cursor = 0
        for right_cursor in range(len(text)):
            if text[right_cursor] == " ":
                if not self.fit_inner(text[left_cursor : right_cursor + 1]):
                    chars[prevous_cursor] = "\n"
                    left_cursor = right_cursor
                prevous_cursor = right_cursor

        return "".join(chars)

    def inner_centered_top(self) -> int:
        """finds vertical coordinate, for text to be vertically centered inside the image"""
        text_height = self.get_str_height(self.text)
        centered = (self.inner_height - text_height) / 2
        return centered

    def _imprint_text(self, text: str, pos: tuple):
        """Imprints text on image"""
        draw = ImageDraw.Draw(self.bg)
        draw.multiline_text(
            pos,
            text,
            font=self.font,
            fill="black",
            spacing=0,
            stroke_width=1,
            stroke_fill="black",
        )
        return self

    def imprint_text(self):
        """imprints text in the middle of the inner box"""
        return self._imprint_text(
            text=self.text, pos=(self.inner_left, self.inner_centered_top()),
        )

    def imprint_signature(self):
        """imprints signature in the right-bottom corner of the inner box"""
        return self._imprint_text(
            text=self.signature,
            pos=(
                self.inner_right - self.get_str_width(self.signature),
                self.inner_bottom - self.get_str_height(self.signature),
            ),
        )

    def show(self, *args, **kwargs):
        self.bg.show(*args, **kwargs)


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
        iic.signature = author
        iic.imprint_text().imprint_signature().show()
        break
