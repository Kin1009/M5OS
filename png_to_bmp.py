from PIL import Image

def png_to_bmp(png_path, bmp_path=None):

    if bmp_path is None:
        bmp_path = png_path.rsplit(".", 1)[0] + ".bmp"

    img = Image.open(png_path).convert("RGBA")

    bg = (17, 17, 17)

    out = Image.new("RGB", img.size, bg)
    out.paste(img, mask=img.getchannel("A"))

    out.save(bmp_path, "BMP")

    return bmp_path


png_to_bmp("logo.png")