import xml.etree.ElementTree as ET
import os
from PIL import Image, ImageDraw, ImageFont


def parse_rec(pic_path, filename):
    """解析xml"""
    tree = ET.parse(filename)  # 解析读取xml函数
    objects = []
    img_dir = []
    coordinate = []
    for xml_name in tree.findall('filename'):
        img_path = os.path.join(pic_path, xml_name.text)
        img_dir.append(img_path)
    for obj in tree.findall('object'):
        obj_struct = {'name': obj.find('name').text, 'pose': obj.find('pose').text,
                      'truncated': int(obj.find('truncated').text), 'difficult': int(obj.find('difficult').text)}
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)
    for obj_one in objects:
        xmin = int(obj_one['bbox'][0])
        ymin = int(obj_one['bbox'][1])
        xmax = int(obj_one['bbox'][2])
        ymax = int(obj_one['bbox'][3])
        label = obj_one['name']
        coordinate.append([xmin,ymin,xmax,ymax,label])
    return coordinate, img_dir


def visualise_gt(objects, img_dir, now_path, font):
    """可视化"""
    for _, img_path in enumerate(img_dir):
        img = Image.open(img_path)
        draw = ImageDraw.ImageDraw(img)
        for obj in objects:
            xmin = obj[0]
            ymin = obj[1]
            xmax = obj[2]
            ymax = obj[3]
            label = obj[4]
            draw.rectangle(((xmin, ymin), (xmax, ymax)), fill=None, outline="red")
            draw.text((xmin + 10, ymin), label, "blue", font=font)  # 利用ImageDraw的内置函数，在图片上写入文字
            img.save(os.path.join(now_path + '/' + os.path.split(img_path)[-1]))
        # img.show(img_path)


if __name__ == "__main__":
    # 图片路径
    pic_path = r"./Math/JPEGImages"
    # xml文件路径
    ann_path = r"./Math/Annotations"
    # 解析后存放地址
    now_path = r"./Math/Now"
    # 字体路径
    fontPath = r"C:\Windows\Fonts\Consolas\consola.ttf"
    font = ImageFont.truetype(fontPath, 20)

    for filename in os.listdir(ann_path):
        xml_path = os.path.join(ann_path, filename)
        # obj_context：返回一个含有所有标注的信息，img_dir：原始图片路径
        obj_context, img_dir = parse_rec(pic_path, xml_path)
        # print("object:", obj_context)
        # print("img_dir:", img_dir)
        visualise_gt(obj_context, img_dir, now_path, font)
