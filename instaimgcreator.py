from PIL import Image, ImageFont

from fontedtext import FontedText, FontedTextPrinter


class MyQuoteText(FontedText):
    def __init__(self, text: str) -> None:
        self.text = text
        self.color = (0, 0, 0, int(255 * 0.86))
        self.font = ImageFont.truetype("DancingScript-SemiBold.ttf", 140)
        self.stroke_size = 1
        self.spacing = 0
        self.shadow = (0, 0, 0, int(255 * 0.3)), (-4, 4)

        self.text_wrap(861)


class MyAuthorText(FontedText):
    def __init__(self, text: str) -> None:
        self.text = text if text.startswith("-") else f"-{text}"
        self.color = (0, 0, 0, int(255 * 0.86))
        self.font = ImageFont.truetype("Brush Script.ttf", 86)
        self.stroke_size = 1
        self.spacing = 0
        self.shadow = (0, 0, 0, int(255 * 0.3)), (-4, 4)


class MyInstaImgCreator:
    def __init__(
        self, text: str = "", quote: str = "", image: Image.Image = None
    ) -> None:
        self._quote = MyQuoteText(text)
        self._author = MyAuthorText(quote)
        self.image = image if image else None
        self.printer = FontedTextPrinter()

        self.inner_left = 110
        self.inner_right = 971
        self.inner_width = self.inner_right - self.inner_left
        self.inner_top = 130
        self.inner_bottom = 1168
        self.inner_height = self.inner_bottom - self.inner_top

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

    def _centered_top(self, text: FontedText) -> int:
        """finds vertical coordinate, for text to be vertically centered inside the image"""
        centered = (self.image.size[1] - text.height) / 2
        return centered

    def _quote_pos(self) -> tuple:
        left = self.inner_left
        top = self._centered_top(self.quote)
        return left, top

    def _author_pos(self) -> tuple:
        """Right Bottom corner of inner box"""
        left = self.inner_right - self.author.width
        top = self.inner_bottom - self.author.height
        return left, top

    def _quote_printer(self) -> None:
        self.printer.text = self.quote
        self.printer.position = self._quote_pos()
        self.printer.image = self.image

    def _author_printer(self, img=None) -> None:
        self.printer.text = self.author
        self.printer.position = self._author_pos()
        if img:
            self.printer.image = img
        else:
            self.printer.image = self.image

    def get_complete_image(self) -> Image.Image:
        self._quote_printer()
        image = self.printer.print()
        # image = self.printer.print(commit=False)
        self._author_printer(image)
        image = self.printer.print()
        return image
