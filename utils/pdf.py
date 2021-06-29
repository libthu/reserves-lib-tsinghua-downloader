from io import BytesIO
from PIL import Image


def generate_pdf(path, imgs) -> None:
    file = BytesIO()
    for img_list in imgs:
        for bin in img_list:
            img = Image.open(BytesIO(bin))
            img.convert('RGB').save(file, append=True)
    file.seek(0)
    with open(path, 'wb') as f:
        f.write(file.read())
