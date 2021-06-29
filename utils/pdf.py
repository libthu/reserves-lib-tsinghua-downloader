from io import BytesIO
from PIL import Image


def generate_pdf(path: str, imgs) -> None:
    file = BytesIO()
    cnt = 0
    for img_list in imgs.values():
        for bin in img_list:
            img = Image.open(BytesIO(bin))
            img.convert('RGB').save(file, format='pdf', append=True)
            cnt = cnt + 1
            if cnt % 100 == 0:
                print(cnt)
    file.seek(0)
    with open(path, 'wb') as f:
        f.write(file.read())
