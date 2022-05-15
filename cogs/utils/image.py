import numpy
from PIL import Image, ImageDraw, ImageFont


def text_to_png(text: str, fp="./image_gen/image_gen.png", size=12, color=(255,255,0), font='./image_gen/Minecraftia-Regular.ttf'):
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
    image = Image.new(mode = "RGB", size = fnt.getsize(text), color = "black")
    draw = ImageDraw.Draw(image)
    draw.text((0,0), text, font=fnt, fill=color)
    image.save(fp)
 
def transparency(fp="./image_gen/image_gen.png"):
    """Turns an image into a transparent image

    Args:
        fp (str, optional): Path to the image to transparentify. Defaults to "./image_gen/image_gen.png".
    """
    img = Image.open(fp)
    rgba = img.convert("RGBA")
    data = rgba.getdata()
  
    newData = []
    for item in data:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
            # storing a transparent value when we find a black colour
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)  # other colours remain unchanged
    
    rgba.putdata(newData)
    rgba.save("./image_gen/transparent_image_gen.png", "PNG")

class TextBox:
    """Represents a text box
    
    Attributes:
        pos (tuple): (x,y) coordinates of the top left corner of the box.
        dimensions (tuple): (width, height) of the box.
        font (str): Path to the font to use.
        fontsize (int, optional): Fontsize. Defaults to 14.
        allowWrap (bool, optional): Whether or not to allow text to wrap and shrink to avoid overflowing container. Defaults to True.
        angle (int, optional): Angle of the text. Defaults to 0.
        skew (int, optional): Skew of the text. Defaults to 0.
        text_color (tuple, optional): Color of the text. Defaults to (0,0,0).
        optional (bool, optional): Whether the text box is optional. Defaults to False.
    """
    def __init__(self, pos, dimensions, font, fontsize=14, allowWrap=True, angle=0, skew=0, text_color=(0,0,0), optional=False):
        self.pos = pos
        self.dimensions = dimensions
        self.font = font
        self.fontsize = fontsize
        self.allowWrap = allowWrap
        self.angle = angle
        self.skew = skew
        self.text_color = text_color
        self.optional = optional
        
def draw_text_to_image(TextBox, text, fp="./image_gen/image_gen.png"):
    """Draws a text box with the given text to an image
    
    Args:
        TextBox (TextBox): The text box to draw.
        text (str): The text to draw.
        fp (str): Path to the image to draw the text on top of.
    """
    img = Image.open(fp)
    draw = ImageDraw.Draw(img)
    if TextBox.allowWrap:
        lines, fontsize = resize_and_wrap(text, TextBox)
        textWrapped = "\n".join(lines)
        font = ImageFont.truetype(TextBox.font, fontsize)
    else:
        font = ImageFont.truetype(TextBox.font, TextBox.fontsize)
    # Todo: draw angled/skewed text
    if (TextBox.angle == 0) and (TextBox.skew == 0):
        # If the text is not skewed or rotated, we can use the built-in function
        draw.multiline_text((TextBox.pos[0], TextBox.pos[1]), textWrapped, font=font, fill=TextBox.text_color)
    else:
        # Not implemented yet
        raise NotImplementedError("TextBox is skewed or rotated. You should really get that looked at.")
        # draw.multiline_text((TextBox.pos[0], TextBox.pos[1]), textWrapped, font=font, fill=TextBox.text_color)
    img.save(fp)

def wrap_text(text, width, font: ImageFont):
    """Wraps text to a given width.
    
    Args:
        text (str): The text to wrap.
        width (int): The width to wrap to.
        font (ImageFont): The font to use.
    
    Returns:
        list: Lines of wrapped text.
        int: The height of the text.
        
    Throws:
        ValueError: If the text is too long to fit in the given width.
    """
    lines = []
    height = 0
    line = ""

    for word in text.split():
        if font.getsize(line + word)[0] > width:
            lines.append(line)
            height += font.getsize(line)[1]
            line = word + " "
        else:
            line += word + " "
    if font.getsize(line + word)[0] > width:
        raise ValueError("Text is too long to fit in the given width.")        
    lines.append(line)
    height += font.getsize(line)[1]
    return lines, height
    
def resize_and_wrap(text, box: TextBox):
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
    try:
        lines, height = wrap_text(text, box.dimensions[0], font)
    except ValueError:
        # Text is simply too thicc. We need to go smaller until it isn't.
        while True:
            try:
                font = ImageFont.truetype(box.font, font.size-1)
                lines, height = wrap_text(text, box.dimensions[0], font)
                break
            except ValueError:
                continue
    if height > box.dimensions[1]:
        # Text is taller than the box, we can't fit it. Let's try again, but smaller.
        while height > box.dimensions[1]:
            font = ImageFont.truetype(box.font, font.size-1)
            lines, height = wrap_text(text, box.dimensions[0], font)
        # Now it should fit.
        return lines, font.size
    else:
        # Otherwise, we can fit it without any shenanigans. Yay!
        return lines, font.size
        
# function copy-pasted from https://stackoverflow.com/a/14178717/744230
def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0]*t[0], -s[0]*t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1]*t[0], -s[1]*t[1]])
    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)
