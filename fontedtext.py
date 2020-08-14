from typing import Optional
from PIL import Image, ImageDraw, ImageFilter, ImageFont


class FontedText:
    """Text and Font in one + optional shadow."""

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
        self.text: str = text
        self.color: tuple = color
        self.font: ImageFont = ImageFont.truetype(font, font_size)
        self.stroke_size: int = stroke_size
        self.spacing: int = spacing
        self._shadow: tuple = (shadow_color, shadow_offset)

    @property
    def width(self) -> int:
        """Width of text."""
        return self.font.getsize_multiline(self.text)[0]

    @property
    def height(self) -> int:
        """Height of text."""
        return self.font.getsize_multiline(self.text)[1]

    @property
    def size(self) -> tuple:
        """Width, Height of text.
        
        size: tuple(width, height)
        """
        return self.font.getsize_multiline(self.text)

    @property
    def shadow(self) -> tuple:
        """Shadow properties of a text.
        
            tuple(color, offset)
                color: tuple(R, G, B, A)
                offset: tuple(left, top)
        
        shadow can be used to achieve interesting effects, if use color different
        from text color
        """
        return self._shadow

    @shadow.setter
    def shadow(self, *args) -> None:
        self._shadow = args[0][0], args[0][1]

    def shadow_color(self) -> tuple:
        """Color of the shadow."""
        return self._shadow[0]

    def shadow_offset(self) -> tuple:
        """Offset of the shadow."""
        return self._shadow[1]

    @property
    def has_shadow(self) -> bool:
        """Check if both shadow properties are set."""
        return not (self._shadow[0][0] is None or self._shadow[0][1] is None)

    def text_wrap(self, width: int) -> None:
        """Wrap text, so it would fit given width."""
        chars = list(self.text)
        left_cursor = 0
        prevous_cursor = 0
        for right_cursor in range(len(self.text)):
            if (
                self.text[right_cursor] == " "
                or right_cursor == len(self.text) - 1
            ):
                if not self._is_fit(
                    self.text[left_cursor : right_cursor + 1], width
                ):
                    chars[prevous_cursor] = "\n"
                    left_cursor = prevous_cursor + 1
                prevous_cursor = right_cursor
        self.text = "".join(chars)

    def _is_fit(self, text: str, width: int) -> bool:
        """Check if text fits into given width."""
        return self.font.getsize_multiline(text)[0] <= width


class FontedTextPrinter:
    """Prints FontedText to Image.

    print() -> PIL.Image.Image
    """

    def __init__(
        self,
        text: FontedText = None,
        position: tuple = None,
        image: Image.Image = None,
    ) -> None:
        """???.

        Args:
            text (FontedText, optional): A text. Defaults to None.
            position (tuple, optional): A position. Defaults to None.
            image (Image.Image, optional): An Image. Defaults to None.
        """
        self._text = text
        self._position = position
        self._image = image

    @property
    def text(self) -> FontedText:
        """Text, what will be printed on an image."""
        return self._text

    @text.setter
    def text(self, text: FontedText) -> None:
        self._text = text

    @property
    def position(self) -> tuple:
        """Position on an image, where text will be printed.
        
        position: tuple(left: int, top: int)
        """
        return self._position

    @position.setter
    def position(self, position: tuple) -> None:
        self._position = position

    @property
    def image(self) -> Image.Image:
        """Image, where text will be printed."""
        return self._image

    @image.setter
    def image(self, image: Image.Image) -> None:
        self._image = image

    def _shadow_pos(self) -> Optional[tuple]:
        """Return position of the shadow."""
        if self.text.has_shadow:
            left = self.position[0] + self.text.shadow_offset()[0]
            top = self.position[1] + self.text.shadow_offset()[1]
            return left, top

    def _get_layer(self) -> Image.Image:
        """Return empty transparent image with size of provided image."""
        return Image.new("RGBA", self.image.size, (255, 255, 255, 0))

    def _to_image(self, position: tuple, color: tuple) -> Image.Image:
        """Return transparent image with printed text."""
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

    def print(self, use_image=True) -> Image.Image:
        """Return image with text on it.

        if use_image is set to True, image will be used,
        otherwise text will br printed on transparent background.
        
        Args:
            use_image (bool, optional): Defaults to True.

        Returns:
            Image.Image: image with text
        """
        image = self._to_image(self.position, self.text.color)

        if self.text.has_shadow:
            shadow = self._to_image(
                self._shadow_pos(), self.text.shadow_color()
            )
            shadow = shadow.filter(ImageFilter.BLUR)
            image = Image.alpha_composite(image, shadow)

        if use_image:
            image = Image.alpha_composite(self.image, image)
        return image
