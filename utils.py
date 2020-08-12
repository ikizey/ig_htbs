""" Helper classes with my settings"""
from PIL import Image, ImageFont

from fontedtext import FontedText, FontedTextPrinter


class MyQuoteText(FontedText):
    """just to reduce constructor code later"""

    def __init__(self, text: str) -> None:
        self.text = text
        self.color = (0, 0, 0, int(255 * 0.76))  # black 76% opacity
        self.font = ImageFont.truetype("DancingScript-SemiBold.ttf", 140)
        self.stroke_size = 1  # bold
        self.spacing = 0  # minium

        # black opacity 30%;
        self.shadow = (0, 0, 0, int(255 * 0.3)), (-4, 4)

        self.text_wrap(851)  # text should fit into this width


class MyAuthorText(FontedText):
    """just to reduce constructor code later"""

    def __init__(self, text: str) -> None:
        self.text = text if text.startswith("-") else f"-{text}"  # prefix with -
        self.color = (0, 0, 0, int(255 * 0.76))  # black 76% opacity
        self.font = ImageFont.truetype("Brush Script.ttf", 86)
        self.stroke_size = 1  # bold
        self.spacing = 0  # minimum
        # black opacity 30%;
        self.shadow = (0, 0, 0, int(255 * 0.3)), (-4, 4)


class MyInstaImgCreator:
    """class that generates photos via printer"""

    def __init__(
        self, text: str = "", quote: str = "", image: Image.Image = None
    ) -> None:
        self._quote = MyQuoteText(text)
        self._author = MyAuthorText(quote)
        self.image = image if image else None
        self.printer = FontedTextPrinter()

        # inner box: only this part of image can be seen in preview
        self.inner_left = 115
        self.inner_right = 966
        self.inner_top = 134
        self.inner_bottom = 1159
        self.inner_height = self.inner_bottom - self.inner_top
        self.inner_width = self.inner_right - self.inner_left

    @property
    def quote(self) -> FontedText:
        return self._quote

    @quote.setter
    def quote(self, text: str) -> None:
        self._quote = MyQuoteText(text)

    @property
    def author(self) -> FontedText:
        return self._author

    @author.setter
    def author(self, text: str) -> None:
        self._author = MyAuthorText(text)

    # this might belong to printer class
    def _centered_top(self, text: FontedText) -> int:
        """finds vertical coordinate, for text to be vertically centered inside the image"""
        centered = (self.inner_height - text.height) / 2 + self.inner_top

        return centered

    def _quote_pos(self) -> tuple:
        left = self.inner_left
        top = self._centered_top(self.quote)
        return left, top

    def _quote_printer(self) -> None:
        """setup printer with quote information and initial image"""
        self.printer.text = self.quote
        self.printer.position = self._quote_pos()
        self.printer.image = self.image

    def _author_pos(self) -> tuple:
        """Right Bottom corner of inner box"""
        left = self.inner_right - self.author.width
        top = self.inner_bottom - self.author.height
        return left, top

    def _author_printer(self, img=None) -> None:
        """setup printer with author information and image"""
        self.printer.text = self.author
        self.printer.position = self._author_pos()
        if img:
            self.printer.image = img
        else:
            self.printer.image = self.image

    def get_complete_image(self) -> Image.Image:
        """Creates final image"""

        # setup printer with quote text and font settings
        self._quote_printer()

        # get image with text
        image = self.printer.print()

        # setup printer with author text and font settings
        # but use prevous image instead of initial
        self._author_printer(image)

        # get another image with author text added
        image = self.printer.print()

        return image
