import cv2
import os
import numpy as np
import traceback
from time import *
import winsound
import pyttsx3


# s1,s2：就是识别人的名字
subjects = ["stranger", "hfp", "lc"]


def menu():
    """菜单"""
    print("*"*10 + "人脸识别系统" + "*"*10)
    print("*"*10 + "菜单" + "*"*10)
    print("*"*5 + "1、进行检测" + "*"*8)
    print("*"*5 + "2、输入图片检测" + "*"*5)
    print("*"*5 + "3、录入人脸信息" + "*"*5)
    print("*"*5 + "4、重新训练预测" + "*"*5)
    print("*"*5 + "5、退出" + "*" * 12)
    print("*"*30)


def catchPICFromVideo(addr):
    """截取图片"""
    cap = cv2.VideoCapture(0)
    # 告诉OpenCV使用人脸识别分类器
    classfier = cv2.CascadeClassifier(r'G:\Opencv 4.5.3\opencv\build\etc\lbpcascades\lbpcascade_frontalface_improved'
                                      r'.xml')
    rect_color = (0, 255, 0)
    num = 1
    while cap.isOpened():
        _, frame = cap.read()
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将当前桢图像转换成灰度图像
        faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=20, flags=4)
        print("11", faceRects)
        if len(faceRects) > 0:  # 大于0则检测到人脸
            for faceRect in faceRects:  # 单独框出每一张人脸
                print("22",faceRect)
                x, y, w, h = faceRect
                # print(x, y, w, h)
                # 将当前帧保存为图片
                img_name = r'%s\%d.jpg ' % (addr + "/", num)
                print("33",img_name)
                image = frame[y - 100: y + h + 40, x - 60: x + w + 80]
                cv2.imwrite(img_name, image)
                sleep(0.05)
                cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), rect_color, 2)
                # 显示当前捕捉到了多少人脸图片了
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'num:%d' % num, (x + 30, y + 30), font, 1, (255, 0, 255), 4)
                num += 1
                # 如果超过指定最大保存数量退出循环
                if num > 200: 
                    break

        # 超过指定最大保存数量结束程序
        if num > 200:  # to_noNeed
            break

        # 显示图像
        cv2.imshow("photo", frame)
        c = cv2.waitKey(10)
        if c == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def detect_face(img):
    """使用OpenCV检测人脸的函数"""
    # 转化为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用LBP分类器，还有一种更精确但速度较慢的Haar分类器
    face_cascade = cv2.CascadeClassifier(r'G:\Opencv 4.5.3\opencv\build\etc\lbpcascades\lbpcascade_frontalface.xml')  # todo
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    if len(faces) == 0:
        return None

    # 假设就只有一张人脸
    (x, y, w, h) = faces[0]
    return gray[y:y + w, x:x + h], faces[0]


def prepare_training_data(data_folder_path):
    """读取所有人员的训练图像,从每个图像中检测人脸，并返回两个大小完全相同的列表，一个人脸列表和另一个人脸标签列表"""
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    for dir_name in dirs:
        if not dir_name.startswith("tupian"):
            continue
        label = int(dir_name.replace("tupian", ""))
        # 得到当前的图像文件的一个地址
        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue
            # 得到当前图片的地址
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            # cv2.imshow("image", image)
            cv2.waitKey(100)
            try:
                face, rect = detect_face(image)
            except:
                pass
            else:
                # 忽略为检测到的人脸
                if face is not None:
                    faces.append(face)
                    labels.append(label)

    # cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    return faces, labels


def draw_rectangle(img, rect):
    """矩形绘制"""
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


def draw_text(img, text, x, y):
    """文本绘制"""
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 3)


def predict(face_recognizer, subjects):
    """识别所传递图像中的人物，并在检测到的人脸周围绘制一个带有对象名称的矩形"""
    # 加载训练好的模型
    face_recognizer.read(r'./models/train.yml')
    addr = input("请输入图片地址：")
    # 读取图片
    test_img = cv2.imread(addr)
    # 复制图像，因为我们不想更改原始图像
    test_img = test_img.copy()
    try:
        # 有时会因为环境因素导致报错，加一个异常处理
        face, rect = detect_face(test_img)
    except Exception as e:
        print("错误信息为：", e)
        traceback.print_exc()
        print('traceback.format_exc():\n%s' % traceback.format_exc())
    else:
        # 进行预测，得到标签和置信度
        label = face_recognizer.predict(face)
        # 得到预测姓名
        label_text = subjects[label[0]]
        # 画矩形框
        draw_rectangle(test_img, rect)
        # 在图片上填上预测的姓名
        draw_text(test_img, label_text, rect[0], rect[1] - 5)
        # 进行显示
        cv2.imshow("predict", test_img)

        # 按下q键退出显示
        key = cv2.waitKey(0)
        if key == ord("q"):
            cv2.destroyAllWindows()


def realTimeIdentification(face_recognizer, subjects):
    """实时识别"""
    print("进行实时预测")
    face_recognizer.read(r'./models/train.yml')
    cap = cv2.VideoCapture(0)
    # 视频保存 保存的文件的路径 fourcc:指定编码器 fps:要保存的视频的帧率 frameSize:要保存的文件的画面尺寸 isColor:指示是黑白画面还是彩色的画面
    fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
    out = cv2.VideoWriter(r'./output.avi', fourcc, 20.0, (640, 480), True)
    # 循环检测识别人脸
    start_time = time()
    while True:
        _, frame = cap.read()
        sleep(0.01)
        try:
            face, rect = detect_face(frame)
            label = face_recognizer.predict(face)
        except Exception as e:
            print("错误信息为：", e)
            traceback.print_exc()
            print('traceback.format_exc():\n%s'%traceback.format_exc())
            cv2.imshow('camera', frame)
        else:
            print(label)
            if label[1] > 80:
                engine = pyttsx3.init()
                end_time = time()
                draw_rectangle(frame, rect)
                draw_text(frame, subjects[0], rect[0], rect[1] - 5)
                out.write(frame)
                run_time = end_time - start_time
                if frame is not None and run_time > 10:
                    winsound.Beep(1440, 1500)  # 主板蜂鸣器
                    engine.say("警告，警告，有陌生人靠近")
                    engine.runAndWait()
                    start_time = end_time
            else:
                label_text = subjects[label[0]]
                draw_rectangle(frame, rect)
                draw_text(frame, label_text, rect[0], rect[1] - 5)

        cv2.imshow('camera', frame)
        # 等待10毫秒看是否有按键输入
        k = cv2.waitKey(10)
        # 如果输入q则退出循环
        if k & 0xFF == ord('q'):
            break

    # 释放摄像头并销毁所有窗口
    out.release()
    cap.release()
    cv2.destroyAllWindows()


def train(face_recognizer):
    """训练数据"""
    print("数据准备")
    faces, labels = prepare_training_data(r"./train_data")
    print("准备完成")
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))
    print("开始训练")
    # 训练人脸识别器
    face_recognizer.train(faces, np.array(labels))
    # 保存训练好的模型
    face_recognizer.save(r"./models/train.yml")
    print("训练完成")


def InputInformation(face_recognizer, subjects):
    name = input("请输入录入的名字：")
    subjects.append(name)
    num = len(os.listdir(r"./train_data/"))
    if not os.path.exists(r"./train_data/tupian"+str(num+1)):
        os.makedirs(r"./train_data/tupian"+str(num+1))
    print("请耐心等待一会")  # 约80秒
    catchPICFromVideo(r"./train_data/tupian"+str(num+1))
    train(face_recognizer)


def main():
    # LBPH面都识别
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    while True:
        num = eval(input("请输入对应的数字："))
        if num == 1:
            realTimeIdentification(face_recognizer, subjects)
        elif num == 2:
            predict(face_recognizer, subjects)
        elif num == 3:
            InputInformation(face_recognizer, subjects)
            realTimeIdentification(face_recognizer, subjects)
        elif num == 4:
            train(face_recognizer)
            predict(face_recognizer, subjects)
        elif num == 5:
            print("欢迎下次再来！")
            break


if __name__ == "__main__":
    menu()
    main()


# EigenFaces人脸识别器
# face_recognizer = cv2.face.EigenFaceRecognizer_create()
# FisherFaces人脸识别器
# face_recognizer = cv2.face.FisherFaceRecognizer_create()
