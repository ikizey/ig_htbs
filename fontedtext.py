from PIL import Image, ImageDraw, ImageFilter, ImageFont


class FontedText:
    """Combines ImageFont, and str into single entity"""

    def __init__(
        self,
        text: str,
        color: tuple,
        font: str,
        font_size: int = 14,
        stroke_size: int = 0,
        spacing: int = 0,
        shadow_color: tuple = None,
        shadow_offset: tuple = None,
    ) -> None:
        self._text: str = text
        self.color: tuple = color
        self.font: ImageFont = ImageFont.truetype(font, font_size)
        self.stroke_size: int = stroke_size
        self.spacing: int = spacing
        self._shadow: tuple = (shadow_color, shadow_offset)

    @property
    def text(self) -> str:
        """Returns text"""
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        """Sets text"""
        self._text = text

    @property
    def width(self) -> int:
        """Returns width of text"""
        return self.font.getsize_multiline(self.text)[0]

    @property
    def height(self) -> int:
        """Returns height of text"""
        return self.font.getsize_multiline(self.text)[1]

    @property
    def size(self) -> tuple:
        """Returns size of text"""
        return self.font.getsize_multiline(self.text)

    @property
    def shadow(self) -> tuple:
        """Returns `tuple: (color, offset)`
        where `color: tuple(R, G, B, A)`;
        `offset: tuple(left, top)`
        
        This can be used to achieve interesting effects, 
        if use color different from text color
        """
        return self._shadow

    @shadow.setter
    def shadow(self, *args) -> None:
        """ Sets shadow properties:
        `args: tuple(shadow_color, shadow_offset)`
        where `color: tuple(R, G, B, A)`;
        `offset: tuple(left, top)`
        """
        self._shadow = args[0][0], args[0][1]

    def shadow_color(self) -> tuple:
        """Returns color of the shadow"""
        return self._shadow[0]

    def shadow_offset(self) -> tuple:
        """Returns offset of the shadow"""
        return self._shadow[1]

    @property
    def has_shadow(self):
        """Checks if color and offset is present"""
        return not (self._shadow[0][0] is None or self._shadow[0][1] is None)

    def text_wrap(self, width: int) -> None:
        """Wraps text, so it would fit given width"""

        chars = list(self.text)
        left_cursor = 0
        prevous_cursor = 0
        for right_cursor in range(len(self.text)):
            if self.text[right_cursor] == " " or right_cursor == len(self.text) - 1:
                if not self._is_fit(self.text[left_cursor : right_cursor + 1], width):
                    chars[prevous_cursor] = "\n"
                    left_cursor = prevous_cursor + 1
                prevous_cursor = right_cursor
        self.text = "".join(chars)

    def _is_fit(self, text: str, width: int) -> bool:
        """Checks if text fits into given width"""
        return self.font.getsize_multiline(text)[0] <= width

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}::{self.text}>"


class FontedTextPrinter:
    """Prints FontedText to Image

    `print -> PIL.Image.Image`"""

    def __init__(
        self, text: FontedText = None, position: tuple = None, image: Image.Image = None
    ) -> None:
        """`text: FontedText`;
        `position: tuple(left, top, right, bottom)`;
        `image: PIL.Image.Image`
        """
        self._text = text
        self._position = position
        self._image = image

    @property
    def text(self) -> FontedText:
        return self._text

    @text.setter
    def text(self, text: FontedText) -> None:
        self._text = text

    @property
    def position(self) -> tuple:
        return self._position

    @position.setter
    def position(self, position: tuple) -> None:
        self._position = position

    @property
    def image(self) -> Image.Image:
        """Returns `image -> PIL.Image.Image`"""
        return self._image

    @image.setter
    def image(self, image: Image.Image) -> None:
        """Sets image
        `image: PIL.Image.Image`"""

        self._image = image

    def _shadow_pos(self) -> tuple:
        """Returns position of the shadow"""
        if self.text.has_shadow:
            left = self.position[0] + self.text.shadow_offset()[0]
            top = self.position[1] + self.text.shadow_offset()[1]
            return left, top

    def _get_layer(self) -> Image.Image:
        """Returns empty transparent image of given size"""
        return Image.new("RGBA", self.image.size, (255, 255, 255, 0))

    def _to_image(self, position: tuple, color: tuple) -> Image.Image:
        """Returns image of given size
        with text at given position with transparent backgorund"""
        layer = self._get_layer()
        draw = ImageDraw.Draw(layer)
        draw.multiline_text(
            position,
            self.text.text,
            font=self.text.font,
            fill=color,
            spacing=self.text.spacing,
            stroke_width=self.text.stroke_size,
            stroke_fill=color,
        )
        return layer

    def print(self, commit=True) -> Image.Image:
        """Returns image with text on it.

        If `commit == True`, get initial image with text on it
        otherwise, get an image with text on tansparent background
        """
        image = self._to_image(self.position, self.text.color)

        if self.text.has_shadow:
            shadow = self._to_image(self._shadow_pos(), self.text.shadow_color())
            shadow = shadow.filter(ImageFilter.BLUR)
            image = Image.alpha_composite(image, shadow)

        if commit:
            image = Image.alpha_composite(self.image, image)
        return image
