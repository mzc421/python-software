import cv2


def Turn_on_the_camera():
    # 调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
    cap = cv2.VideoCapture(0)
    # while True: # 死循环，让其一值读入图片
    while cap.isOpened():  # 判断是否打开摄像头成功 返回值为一个布尔值
        # _: 如果为true，则读取成功，反之不超过；frame: 读取的图片
        _, frame = cap.read()  # 读取一帧一帧的图像，放回值是一个布尔值
        cv2.imshow("img", frame)  # 进行显示
        key = cv2.waitKey(1)  # 等待一会 单位为毫秒，表示间隔时间
        if key == ord('q'):  # 按q键退出
            break

    cap.release()  # 释放掉摄像头资源，防止在下次调用时不会出错
    cv2.destroyAllWindows()  # 用来删除窗口的，关闭窗口并取消分配任何相关的内存使用


def cat_photo(path):
    cap = cv2.VideoCapture(0)
    num = 1
    while cap.isOpened():
        _, frame = cap.read()
        cv2.imshow("capture", frame)
        key = cv2.waitKey(1)  # 等待一会 单位为毫秒，表示间隔时间
        if key == ord('c'):
            img_name = f'{path}/{num}.jpg'
            cv2.imwrite(img_name, frame)
            print(f"已拍摄{num}张图片")
            num += 1
        if key == ord('q'):  # 按q键退出
            break

    cap.release()
    cv2.destroyAllWindows()


def Open_image():
    # 载入图像
    img = cv2.imread(r"./car.jpg")
    # 查看像素矩阵
    print("img:\n", img)
    print("*" * 50)
    # 查看形状 返回一个元组（高，宽，通道数）
    print("shape:\n", img.shape)
    print("*" * 50)
    # 打印图像尺寸
    h, w = img.shape[:2]
    print(h, w)


def show_image():
    img = cv2.imread(r"./car.jpg")
    cv2.namedWindow("Image")  # 窗口的名字
    cv2.imshow("Image", img)  # 显示图片
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cvt_color():
    img = cv2.imread(r"./car.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("origin", img)  # 显示原始图片
    cv2.imshow("gray", gray)  # 显示灰度图片
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_image():
    # 载入图像
    img = cv2.imread(r"./car.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('gary_car.jpg', gray)


def save_vedio():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
    out = cv2.VideoWriter(r'./output.avi', fourcc, 20.0, (640, 480), True)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            frame = cv2.resize(frame, (640, 480))
            out.write(frame)
            cv2.imshow('frame', frame)
        else:
            break

        key = cv2.waitKey(10)
        if key == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Turn_on_the_camera()
    cat_photo(r"./photo")
    # Open_image()
    # show_image()
    # cvt_color()
    # save_image()
    # save_vedio()
