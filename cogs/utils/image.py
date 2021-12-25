from PIL import Image, ImageDraw, ImageFont

def text_on_img(fp="./image_gen/image_gen.png", text="Hello", size=12, color=(255,255,0), font='Minecraftia-Regular.ttf'):
	"Draw a text on an Image, saves it, show it"
	fnt = ImageFont.truetype(font, size)
	image = Image.new(mode = "RGB", size = (int(size/1.3)*len(text),size+30), color = "black")
	draw = ImageDraw.Draw(image)
	draw.text((10,10), text, font=fnt, fill=color)
	image.save(fp)
 
def transparency(fp="./image_gen/image_gen.png"):
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