
import numpy as np

from PIL import Image

from settings import IMG_HEIGHT, IMG_WIDTH


def move_background(img):
    # 转化为灰度图
    img = img.convert('L')
    # 去掉背景
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if img.getpixel((x, y)) > 155:
                img.putpixel((x, y), 255)
    return img


def find_up(img, x, y, result):
    result.append((x, y))
    if x < img.size[0] - 1 and y < img.size[1] - 1:
        L = img.getpixel((x, y))
        if img.getpixel((x + 1, y + 1)) == L:
            return find_up(img, x + 1, y + 1, result)
        if img.getpixel((x + 1, y)) == L:
            return find_up(img, x + 1, y, result)
        else:
            return result
    else:
        return result


def find_down(img, x, y, result):
    result.append((x, y))
    if x < img.size[0] - 1 and y < img.size[1] - 1:
        L = img.getpixel((x, y))
        if img.getpixel((x + 1, y)) == L:
            return find_down(img, x + 1, y, result)
        if img.getpixel((x + 1, y - 1)) == L:
            return find_down(img, x + 1, y - 1, result)
        else:
            return result
    else:
        return result


def find_left(img, x, y, result):
    result.append((x, y))
    if x < img.size[0] - 1 and y < img.size[1] - 1:
        L = img.getpixel((x, y))
        if img.getpixel((x, y + 1)) == L:
            return find_left(img, x, y + 1, result)
        if img.getpixel((x - 1, y + 1)) == L:
            return find_down(img, x - 1, y + 1, result)
        else:
            return result
    else:
        return result


def find_right(img, x, y, result):
    result.append((x, y))
    if x < img.size[0] - 1 and y < img.size[1] - 1:
        L = img.getpixel((x, y))
        if img.getpixel((x, y + 1)) == L:
            return find_left(img, x, y + 1, result)
        if img.getpixel((x + 1, y + 1)) == L:
            return find_down(img, x + 1, y + 1, result)
        else:
            return result
    else:
        return result


def move_lines(img):
    # 去掉干扰线
    for x in range(1, img.size[0] - 1):
        for y in range(1, img.size[1] - 1):
            if img.getpixel((x, y)) < 255:
                l = find_up(img, x, y, [])
                if len(l) >= 12:
                    for t in l:
                        img.putpixel(t, 255)
                l = find_down(img, x, y, [])
                if len(l) >= 12:
                    for t in l:
                        img.putpixel(t, 255)
                '''l = find_left(img,x,y,[])
                if len(l)>=15 and abs(l[0][0]-[-1][0])>=4:
                    for t in l:
                        img.putpixel(t,255)
                l = find_right(img,x,y,[])
                if len(l)>=15 and abs(l[0][0]-[-1][0])>=4:
                    for t in l:
                        img.putpixel(t,255)'''

    return img


def twovalue(img, color):
    for x in range(1, img.size[0]):
        for y in range(1, img.size[1]):
            if img.getpixel((x, y)) in color:
                # print((x,y),img.getpixel((x,y)) not in color)
                img.putpixel((x, y), 0)
            else:
                img.putpixel((x, y), 255)
    # 填充数字
    for x in range(img.size[0] - 4):
        for y in range(img.size[1] - 4):
            if y < img.size[1] - 2 and img.getpixel((x, y)) == 0 and img.getpixel((x, y + 2)) == 0:
                img.putpixel((x, y + 1), 0)
            if y < img.size[1] - 4 and img.getpixel((x, y)) == 0 and img.getpixel((x, y + 3)) == 0:
                img.putpixel((x, y + 1), 0)
                img.putpixel((x, y + 2), 0)

    return img


def process_img(img):
    # img = Image.open(img_path)
    # 1————去掉背景
    img = move_background(img)

    # 2————色系选择
    hist = img.histogram()
    color = [i for i in range(len(hist) - 1) if hist[i] >= 8]
    # 3————去掉干扰线
    img = move_lines(img)

    # 4————化为二值图并填充
    img = twovalue(img, color)
    return img


def smartSliceImg(img, count=6, p_w=3):
    w, h = img.size
    pixdata = img.load()
    eachWidth = int(w / count)
    beforeX = 0
    split_imgs = []
    for i in range(count):

        allBCount = []
        nextXOri = (i + 1) * eachWidth

        for x in range(nextXOri - p_w, nextXOri + p_w):
            if x >= w:
                x = w - 1
            if x < 0:
                x = 0
            b_count = 0
            for y in range(h):
                if pixdata[x, y] == 0:
                    b_count += 1
            allBCount.append({'x_pos': x, 'count': b_count})
        sort = sorted(allBCount, key=lambda e: e.get('count'))

        nextX = sort[0]['x_pos']
        box = (beforeX, 0, nextX, h)
        split_imgs.append(img.crop(box))
        beforeX = nextX
    return split_imgs


def clear(img):
    l = []
    # 点降噪
    for x in range(1, img.size[0] - 1):
        for y in range(1, img.size[1] - 1):
            nearDots1 = 0
            L = img.getpixel((x, y))
            if L == img.getpixel((x + 1, y)):
                nearDots1 += 1
            if L == img.getpixel((x - 1, y)):
                nearDots1 += 1
            if L == img.getpixel((x, y + 1)):
                nearDots1 += 1
            if L == img.getpixel((x, y - 1)):
                nearDots1 += 1

            if nearDots1 > 3:
                l.append((x, y))
    for t in l:
        img.putpixel(t, 255)
    return img


def rescale_img(img):
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img = img.convert("RGB")
    img = np.array(img)
    img = img * (1. / 255)
    img = np.expand_dims(img, axis=0)
    return img
