import sys
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

if __name__ == '__main__':
    im = Image.open(sys.argv[1])
    for i, _im in enumerate(crop_image(im)):
        _im.save('{}.jpg'.format(i))
