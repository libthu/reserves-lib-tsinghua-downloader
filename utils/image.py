from io import BytesIO

from PIL import Image


def resize(imgs: list[bytes], quality: int, optimize=True) -> None:
    for i, img_data in enumerate(imgs):
        img = Image.open(BytesIO(img_data))
        with BytesIO() as output:
            img.save(output, format=img.format, quality=quality, optimize=optimize)
            imgs[i] = output.getvalue()
