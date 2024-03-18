from PIL import ImageFont, ImageDraw, Image

def text2Img(text, font, img, x, y, color):
  draw = ImageDraw.Draw(img)
  draw.text((x, y), text, font=font, fill=color)
  return img

# img = text2Img("Hello", ImageFont.truetype("arial.ttf", 12), Image.new("RGB", (100, 100), (255, 255, 255)), 20, 20, (0, 0, 0)) # returns <PIL.Image.Image image mode=RGB size=100x100 at 0x7F3E3C3E3E10>
# img.show()

