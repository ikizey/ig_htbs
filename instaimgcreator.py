from PIL import Image, ImageDraw, ImageFont, ImageFilter


class InstaImgCreator:
    def __init__(
        self,
        font_name: str,
        font_size: int,
        signature_font_name: str,
        signature_font_size: int,
        bg_path: str,
        text: str = "",
        signature: str = "",
    ) -> None:
        self.font = ImageFont.truetype(font_name, font_size)
        self.signature_font = ImageFont.truetype(
            signature_font_name, signature_font_size
        )

        self.bg = Image.open(bg_path).convert("RGBA")

        # self._inner_box_coords = (110, 130, 971, 1168)
        self.inner_left = 110
        self.inner_right = 971
        self.inner_width = self.inner_right - self.inner_left
        self.inner_top = 130
        self.inner_bottom = 1168
        self.inner_height = self.inner_bottom - self.inner_top

        self.signature = signature
        self.text = text

    def text_layer(self):
        return Image.new("RGBA", self.bg.size, (255, 255, 255, 0))

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = self.text_wrap(text)

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
        centered = (self.bg.size[1] - text_height) / 2
        return centered

    def _imprint_text(self, text: str, pos: tuple, font: ImageFont):
        """Imprints text on image"""
        layer = self.text_layer()
        draw = ImageDraw.Draw(layer)
        draw.multiline_text(
            (pos[0] + 3, pos[1] + 3),
            text,
            font=font,
            fill=(0, 0, 0, int(255 * 0.3)),
            spacing=0,
            stroke_width=1,
            stroke_fill=(0, 0, 0, int(255 * 0.3)),
        )
        shadow = layer.filter(ImageFilter.BLUR)
        self.bg = Image.alpha_composite(self.bg, shadow)
        ###
        layer = self.text_layer()
        draw = ImageDraw.Draw(layer)
        draw.multiline_text(
            pos,
            text,
            font=font,
            fill=(0, 0, 0, int(255 * 0.7)),
            spacing=0,
            stroke_width=1,
            stroke_fill=(0, 0, 0, int(255 * 0.7)),
        )
        ###

        self.bg = Image.alpha_composite(self.bg, layer)

        return self

    def imprint_text(self):
        """imprints text in the middle of the inner box"""
        left = self.inner_left
        top = self.inner_centered_top()
        return self._imprint_text(text=self.text, pos=(left, top), font=self.font)

    def imprint_signature(self):
        """imprints signature in the right-bottom corner of the inner box"""
        left = (
            self.inner_right - self.signature_font.getsize_multiline(self.signature)[0]
        )
        top = (
            self.inner_bottom - self.signature_font.getsize_multiline(self.signature)[1]
        )
        return self._imprint_text(
            text=self.signature, pos=(left, top), font=self.signature_font
        )

    def show(self, *args, **kwargs):
        self.bg.show(*args, **kwargs)
