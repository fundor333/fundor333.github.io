from PIL import Image, ImageDraw, ImageFont  # 👉️ Import modules from PIL
import typer


def generate_img(message: str, path: str):
    font_path = "Futura Book font.ttf"  # 👉️ Font .ttf Path
    font_size = 100  # 👉️ Font Size
    img = Image.open("cover.jpg")  # 👉️ Open Image
    dr = ImageDraw.Draw(img)  # 👉️ Create New Image
    my_font = ImageFont.truetype(font_path, font_size)  # 👉️ Initialize Font
    text_x = (img.width) // 2
    text_y = (img.height) // 2
    dr.text((text_x, text_y), message, font=my_font, fill=(255, 255, 255), anchor="mm")
    img.save("content/" + path + "/cover.png")


def main(message: str, path: str):
    generate_img(message, path)


if __name__ == "__main__":
    typer.run(main)
