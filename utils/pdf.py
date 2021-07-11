import operator
from functools import reduce

import img2pdf


def generate_pdf(path: str, imgs) -> None:
    img_list = reduce(operator.add, imgs.values())
    with open(path, 'wb') as f:
        f.write(img2pdf.convert(img_list))
