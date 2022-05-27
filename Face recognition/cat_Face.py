import cv2
import time


def CatchPICFromVideo(window_name, catch_num, path_name):
    cv2.namedWindow(window_name)
    cap = cv2.VideoCapture(0)
    # 告诉OpenCV使用人脸识别分类器
    classfier = cv2.CascadeClassifier(r'G:\Opencv 4.5.3\opencv\build\etc\lbpcascades\lbpcascade_frontalface_improved.xml')
    rect_color = (0, 255, 0)
    num = 0
    while cap.isOpened():
        _, frame = cap.read()
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将当前桢图像转换成灰度图像

        # 1、grey：是输入图像
        # 2、scaleFactor：这个是每次缩小图像的比例，默认是1.1 ，我这里选用1.2
        # 3、minNeighbors=15：它表明如果有15个框都重叠一起了，那这里肯定是脸部，当minNeighbors越大时，能适当提高精度
        # 4、minSize()：匹配物体的最小范围   maxSize()：匹配物体的最大范围
        # flags = 0：可以取如下这些值：
        # CASCADE_DO_CANNY_PRUNING = 1, 利用canny边缘检测来排除一些边缘很少或者很多的图像区域
        # CASCADE_SCALE_IMAGE = 2, 正常比例检测
        # CASCADE_FIND_BIGGEST_OBJECT = 4, 只检测最大的物体
        # 这个函数得到的faceRects是一个一维数组[x, y, w, h]分别代表着上左，上右，下左，下右的坐标
        faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=20, flags=4)
        if len(faceRects) > 0:  # 大于0则检测到人脸
            for faceRect in faceRects:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                # print(x, y, w, h)
                # 将当前帧保存为图片
                img_name = r'%s\%d.jpg ' % (path_name, num+201)
                image = frame[y - 100: y + h + 40, x - 60: x + w + 80]
                cv2.imwrite(img_name, image)
                time.sleep(0.05)
                cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), rect_color, 2)
                # 显示当前捕捉到了多少人脸图片了
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'num:%d' % num, (x + 30, y + 30), font, 1, (255, 0, 255), 4)
                num += 1
                if num > catch_num:  # 如果超过指定最大保存数量退出循环
                    break

        # 超过指定最大保存数量结束程序
        if num > catch_num:
            break

        # 显示图像
        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    CatchPICFromVideo("cat_Face", 200, r'new/train_data/tupian2')
