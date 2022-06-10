from PIL import Image
import numpy as np

filename_colour = "薇尔莉特.jpg"
filename_blackWhite = "黑白图片.jpg"


def pil():
    img_colour = Image.open(filename_colour)
    img_blackWhite = Image.open(filename_blackWhite)

    image_colour = np.array(img_colour)
    image_blackWhite = np.array(img_blackWhite)

    # 查看修改前的size和shape
    print("-"*20 + "修改前size" + "-"*20)
    print(filename_colour + " 的size为：", img_colour.size)
    print(filename_blackWhite + " 的size为：", img_blackWhite.size)

    print("-"*20 + "修改前shape" + "-"*20)
    print(filename_colour + " 的shape为：", image_colour.shape)
    print(filename_blackWhite + " 的shape为：", image_blackWhite.shape)

    # 改变尺寸
    out_colour = img_colour.resize((224, 224), Image.ANTIALIAS)
    out_blackWhite = img_blackWhite.resize((224, 224), Image.ANTIALIAS)

    out_image_colour = np.array(out_colour)
    out_image_blackWhite = np.array(out_blackWhite)

    # 查看修改后的size和shape
    print("-" * 20 + "修改后size" + "-" * 20)
    print(filename_colour + " 的size为：", out_colour.size)
    print(filename_blackWhite + " 的size为：", out_blackWhite.size)

    print("-" * 20 + "修改后shape" + "-" * 20)
    print(filename_colour + " 的shape为：", out_image_colour.shape)
    print(filename_blackWhite + " 的shape为：", out_image_blackWhite.shape)

    # 查看通道数
    print("-"*20 + "通道数" + "-"*20)
    print(filename_colour + " 的通道数为：", len(img_colour.split()))
    print(filename_blackWhite + " 的通道数为：", len(img_blackWhite.split()))

    # 保存
    out_colour.save("./薇尔莉特_224.jpg")
    out_blackWhite.save("./黑白图片_224.jpg")


pil()
