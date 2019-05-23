import sys
import random
from PIL import Image

def resize_to_even(im: Image) -> Image:
    '''画像の幅/高さが偶数になるようにcropする'''
    width, height = im.size

    if width % 2 == 1:
        width -= 1
    if height % 2 == 1:
        height -= 1
    
    resized = im.resize((width, height))
    return resized

def crop_image(im: Image) -> [Image]:
    '''画像を4分割する'''
    im = resize_to_even(im)

    width, height = im.size
    half_width = width // 2
    half_height = height // 2

    boxes = [
        (0, 0, half_width, half_height),  # 左上
        (0, half_height, half_width, height),  # 左下
        (half_width, half_height, width, height),  # 右下
        (half_width, 0, width, half_height),  # 右上
    ]

    cropped_imgs = []
    for box in boxes:
        cropped_img = im.crop(box)
        cropped_imgs.append(cropped_img)

    return cropped_imgs

def shuffle_and_concat(ims: [Image]) -> Image:
    '''4つの画像をシャッフルしたり180度反転したりして、
    左上・左下・右下・右上の順に結合する
    '''
    random.shuffle(ims)
    _ims = []
    for im in ims:
        if random.random() < .5:
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
        if random.random() < .5:
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        _ims.append(im)
    ims = _ims
    width, height = ims[0].size
    width *= 2
    height *= 2
    dst = Image.new('RGB', (width, height))
    half_width, half_height = ims[0].size
    dst.paste(ims[0], (0, 0))
    dst.paste(ims[1], (0, half_height))
    dst.paste(ims[2], (half_width, half_height))
    dst.paste(ims[3], (half_width, 0))
    return dst

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    ims = crop_image(im)
    out = shuffle_and_concat(ims)
    out.save('out.jpg')
