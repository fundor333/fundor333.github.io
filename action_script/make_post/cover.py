from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "Futura Book font.ttf"  # 👉️ Font .ttf Path
FONT_SIZE = 100  # 👉️ Font Size


def generate_img(message: str, path: str, image_name: str = "cover.jpg") -> None:
    img = Image.open(image_name)  # 👉️ Open Image
    dr = ImageDraw.Draw(img)  # 👉️ Create New Image
    my_font = ImageFont.truetype(FONT_PATH, FONT_SIZE)  # 👉️ Initialize Font
    text_x = img.width // 2
    text_y = img.height // 2
    dr.text((text_x, text_y), message, font=my_font, fill=(255, 255, 255), anchor="mm")
    output_path = f"content/{path}/cover.png"
    img.save(output_path)
    print(f"Generated {output_path}")
