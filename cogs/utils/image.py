import math
import time

import numpy
from PIL import Image, ImageDraw, ImageFont


class TextBox:
    """Represents a text box

    Attributes:
        pos (tuple): (x,y) coordinates of the top left corner of the box.
        dimensions (tuple): (width, height) of the box.
        font (str): Path to the font to use.
        fontsize (int, optional): Fontsize. Defaults to 14.
        text_color (tuple, optional): Color of the text. Defaults to (0,0,0).
        allowWrap (bool, optional): Whether or not to allow text to wrap and shrink to avoid overflowing container. Defaults to True.
        minFontsize (int, optional): Minimum fontsize before we start breaking words. Defaults to 0.
        angle (int, optional): Angle of the text. Defaults to 0.
        skew (list, optional): Skew of the text. Defaults to no skew.
            Example of skew:    [[(0, 0), (1000, 0), (1000, 1000), (0, 1000)], # Corners of the source image
                                [(50, 550), (250, 20), (250, 450), (50, 250)]] # Corners of the source image after desired skew
        optional (bool, optional): Whether the text box is optional. Defaults to False.
    """

    def __init__(
        self,
        pos,
        dimensions,
        font,
        fontsize=14,
        text_color=(0, 0, 0),
        allowWrap=True,
        minFontsize: int = 0,
        angle: int = 0,
        skew: list = [],
        optional=False,
    ):
        self.pos = pos
        self.dimensions = dimensions
        self.font = font
        if fontsize <= 0:
            raise ValueError("Fontsize must be greater than 0")
        self.fontsize = fontsize
        self.text_color = text_color
        self.allowWrap = allowWrap
        self.minFontsize = minFontsize
        self.angle = angle
        if angle:
            self.skew = 0
        else:
            self.skew = skew
        self.skew = skew
        self.optional = optional


def text_to_png(
    text: str,
    fp="./work/image_gen.png",
    size=12,
    color=(255, 255, 0),
    font="./static/font/Minecraftia-Regular.ttf",
):
    """Writes text to an image

    Args:
        text (str): The text to write.
        fp (str, optional): The path of the file to save to. Defaults to "./image_gen/image_gen.png".
        size (int, optional): Fontsize. Defaults to 12.
        color (tuple, optional): Color of the text. Defaults to (255,255,0).
        font (str, optional): Path to the font to use. Defaults to '/image_gen/Minecraftia-Regular.ttf'.
    """

    fnt = ImageFont.truetype(font, size)
    # image = Image.new(mode = "RGB", size = (int(size/1.3)*len(text),size+30), color = "black")
    image = Image.new(mode="RGB", size=fnt.getsize(text), color="black")
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=fnt, fill=color)
    image.save(fp)


def transparency(fp="./work/image_gen.png"):
    """Turns an image into a transparent image

    Args:
        fp (str, optional): Path to the image to transparentify. Defaults to "./image_gen/image_gen.png".
    """
    img = Image.open(fp)
    rgba = img.convert("RGBA")
    data = rgba.getdata()

    newData = []
    for item in data:
        # finding black colour by its RGB value
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            # storing a transparent value when we find a black colour
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)  # other colours remain unchanged

    rgba.putdata(newData)
    rgba.save("./work/transparent_image_gen.png", "PNG")


def wrap_text(text: str, width: int, font: ImageFont, break_words: bool = False):
    """Wraps text to a given width.

    Args:
        text (str): The text to wrap.
        width (int): The width to wrap to.
        font (ImageFont): The font to use.
        break_words (bool, optional): Whether or not to break words. Defaults to False.

    Returns:
        list: Lines of wrapped text.
        int: The height of the text.

    Throws:
        ValueError: If the text is too long to fit in the given width.
    """
    lines = []
    height = 0
    line = ""
    lineheight = font.getsize("bdfghijklpqty")[1] - 11
    if break_words:
        for letter in list(text):
            if font.getsize(line + letter)[0] > width:
                lines.append(line)
                height += lineheight
                line = letter
            else:
                line += letter
    else:
        for word in text.split():
            if font.getsize(line + word + " ")[0] > width:
                lines.append(line)
                height += lineheight
                line = word + " "
            else:
                line += word + " "
    if font.getsize(line)[0] > width:
        raise ValueError(
            "Text is too long to fit in the given width without overflowing"
        )
    lines.append(line)
    height += font.getsize(line)[1]
    return lines, height


def resize_and_wrap_text(text, box: TextBox):
    """
    Chooses approprate wrapping and fontsize to avoid overflowing a TextBox. Will not exceed the box's given fontsize.

    Args:
        text (str): The text to resize.
        box (TextBox): The TextBox to fit the text inside.

    Returns:
        list: Lines of wrapped text.
        int: Fontsize to use.
    """
    font = ImageFont.truetype(box.font, box.fontsize)
    break_words = False
    try:
        lines, height = wrap_text(text, box.dimensions[0], font)
    except ValueError:
        # Text is simply too thicc. We need to go smaller until it isn't.
        while True:
            try:
                font = ImageFont.truetype(box.font, font.size - 1)
                if font.size <= box.minFontsize:
                    # If our font size goes below our minimum, we can't fit the text in the box without breaking someone's kneecaps. Let's enter KNEECAP BREAKING MODE and try again from the top.
                    break_words = True
                    font = ImageFont.truetype(box.font, box.fontsize)
                lines, height = wrap_text(text, box.dimensions[0], font, break_words)
                break
            except ValueError:
                continue
    if height > box.dimensions[1]:
        # Text is taller than the box, we can't fit it. Let's try again, but smaller.
        while height > box.dimensions[1]:
            font = ImageFont.truetype(box.font, font.size - 1)
            lines, height = wrap_text(text, box.dimensions[0], font, break_words)
        # Now it should fit.
    return lines, font.size


# function copy-pasted from https://stackoverflow.com/a/14178717/744230


def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def draw_text_to_image(
    TextBox,
    text,
    inputPath="./work/image_gen.png",
    outputPath="./image_gen/image_gen.png",
):
    """Draws the given text to an image

    Args:
        TextBox (TextBox): The text box to draw.
        text (str): The text to draw.
        inputPath (str): Path to the image to draw the text on top of. Defaults to "./work/image_gen.png".
        outputPath (str): Path to save the image to. Defaults to "./work/image_gen.png".
    """
    img = Image.open(inputPath)
    draw = ImageDraw.Draw(img)
    if TextBox.allowWrap:
        lines, fontsize = resize_and_wrap_text(text, TextBox)
        textWrapped = "\n".join(lines)
        font = ImageFont.truetype(TextBox.font, fontsize)
    else:
        # This should eventually resize the font without wrapping. Right now it just leaves the fontsize as is, which isn't useful.
        # How would I toggle between wrap/shrink, shrink, and none? Maybe a new attribute?
        textWrapped = text
        font = ImageFont.truetype(TextBox.font, TextBox.fontsize)
    if (TextBox.angle == 0) and (TextBox.skew == 0):
        # If the text is not skewed or rotated, we can use the built-in function
        draw.multiline_text(
            TextBox.pos, textWrapped, font=font, fill=TextBox.text_color, spacing=-4
        )
    else:
        # If the text is rotated or skewed, we need to make a new image, draw the text on it, and then rotate/skew *that*
        img_txt = Image.new("RGBA", TextBox.dimensions, (0, 0, 0, 0))
        draw_txt = ImageDraw.Draw(img_txt)
        draw_txt.multiline_text(
            (0, 0), textWrapped, font=font, fill=TextBox.text_color, spacing=-4
        )
        img_txt = img_txt.rotate(
            TextBox.angle, expand=1, resample=Image.Resampling.BICUBIC
        )

        x = TextBox.pos[0]
        y = TextBox.pos[1]
        angle = math.radians(TextBox.angle % 90)
        # It's rotated, but now the upper-left corner is not near the edge of the text box. We want to take the upper-left corner as input because it's easier for me.
        if 0 <= TextBox.angle % 360 < 90:
            x = TextBox.pos[0]
            y = TextBox.pos[1] - (TextBox.dimensions[0] * math.sin(angle))
        elif 90 <= TextBox.angle % 360 < 180:
            x = TextBox.pos[0] - (TextBox.dimensions[0] * math.sin(angle))
            y = (
                TextBox.pos[1]
                - (TextBox.dimensions[0] * math.cos(angle))
                - (TextBox.dimensions[1] * math.sin(angle))
            )
        elif 180 <= TextBox.angle % 360 < 270:
            x = (
                TextBox.pos[0]
                - (TextBox.dimensions[0] * math.cos(angle))
                - (TextBox.dimensions[1] * math.sin(angle))
            )
            y = TextBox.pos[1] - (TextBox.dimensions[1] * math.cos(angle))
        elif 270 <= TextBox.angle % 360 < 360:
            x = TextBox.pos[0] - (TextBox.dimensions[1] * math.cos(angle))
            y = TextBox.pos[1]

        if img.mode != "RGBA":
            img = img.convert("RGBA")
        img.alpha_composite(img_txt, (math.floor(x), math.floor(y)))
    img.save(outputPath)


def compress_image(
    width,
    height=-1,
    inputPath="./work/image_gen.png",
    outputPath="./work/image_gen.png",
):
    """Compresses an image to given dimensions.

    Args:
        width (int): The width to compress the image to.
        height (int): The height to compress the image to. Defaults to "-1", which preserves the aspect ratio.
        inputPath (str): Path to the image to compress. Defaults to "./work/image_gen.png".
        outputPath (str): Path to save the compressed image to. Defaults to "./work/image_gen.png".
    """
    img = Image.open(inputPath)
    aspect_ratio = img.width / img.height
    if height <= 0:
        height = math.floor(width / aspect_ratio)
    img = img.resize((width, height), Image.ANTIALIAS)
    img = img.convert("P")
    img.save(outputPath, "PNG")


def image_overlay(
    inputPath: str = "./image_gen/image_gen.png",
    outputPath: str = "./image_gen/image_gen.png",
    overlayPath: str = "./image_gen/image_gen.png",
    position: tuple = (0, 0),
):
    """Overlays an image on top of another image with transparency.

    Args:
        inputPath (str): Path to the image to overlay. Defaults to "./image_gen/image_gen.png".
        outputPath (str): Path to save the image to. Defaults to "./image_gen/image_gen.png".
        overlayPath (str): Path to the image to overlay on top of the original image. Defaults to "./image_gen/image_gen.png".
        position (tuple): The position to draw the overlay at. Defaults to (0, 0).
    """
    img = Image.open(inputPath)
    overlay = Image.open(overlayPath)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img.alpha_composite(overlay, (position))
    img.save(outputPath)


# img = Image.open("./test.png")

# coeffs = find_coeffs(
#     [(0, 0), (1000, 0), (1000, 1000), (0, 1000)], #Corners of the source image
#     [(15, 115), (140, 20), (140, 340), (15, 250)]) #Corners of the skewed source image

# img.transform((300, 400), Image.PERSPECTIVE, coeffs,
#               Image.BICUBIC).show()
