import sys
from random import randint
import pygame

pygame.init()  # 初始化

size = w, h = (600, 500)  # 屏幕显示的区域，高度和宽度
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("接球游戏")  # 屏幕的标题
fpsClock = pygame.time.Clock()  # 帧速率 窗口刷新速度 越大运行越快

board = pygame.image.load(r"./挡板.jpg")
board_rect = board.get_rect()  # 对图片进行加框 利用surface生成rect

color = pygame.Color(255, 255, 255)  # 屏幕（窗口）的颜色：白色
Green = pygame.Color('green')  # 小球的颜色：绿色

# 随机生成小球的x、y坐标（整数，包括两端）
ball_x = randint(20, 580)
ball_y = randint(20, 200)

# 小球x、y坐标变化量
move_x = 1
move_y = 1

# 挡板x、y坐标变化量
board_x = 46
board_y = 0

score = 0  # 得分
font = pygame.font.Font(r"./Arial.ttf", 60)  # 设置字体（前者是字体路径）和字体大小
points = 1  # 一次接球的加分
count = 0  # 接球得分的次数

# size1 = board.get_size() #获取图片大小
# print(size1)
while True:
    board_rect.top = h - 17
    for event in pygame.event.get():  # pygame.event.get() 从事件队列中取出事件，并从队列中删除该事件
        if event.type == pygame.QUIT:
            sys.exit()

        # 改变窗口尺寸
        elif event.type == pygame.VIDEORESIZE:
            size = w, h = event.w, event.h
            screen = pygame.display.set_mode(size, pygame.RESIZABLE)


        # 键盘控制挡板
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # 挡板左移
                if board_rect.left > 0 and board_rect.left <= w - 186:
                    board_rect.left -= board_x
                elif board_rect.left <= 0:  # 判断挡板左边的坐标是否小于0
                    board_rect.left = 0
                    board_rect.top -= board_y
            elif event.key == pygame.K_RIGHT:  # 挡板右移
                if board_rect.right >= 186 and board_rect.right < w:
                    board_rect.right += board_x
                elif board_rect.right >= w:  # 判断挡板右边的坐标是否大于屏幕的宽度                        board_rect.right = w
                    board_rect.bottom += board_y

        # 鼠标控制挡板
        elif event.type == pygame.MOUSEMOTION:
            # 鼠标左键按下并跟随鼠标移动
            if event.buttons[0] == 1:
                if event.pos[0] >= 0 and event.pos[0] < w - 186:  # 判断鼠标的位置
                    board_rect.left = event.pos[0]  # 将鼠标的x坐标给Rect对象的左边
                elif event.pos[0] >= w - 186 and event.pos[0] <= w:
                    board_rect.left = w - 186
                # board_rect.top = h - 17 #档板位置在底部
        elif event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标按键按下
            # 将鼠标当前位置给挡板
            if event.button == 1:
                if event.pos[0] >= 0 and event.pos[0] < w - 186:  # 判断鼠标的位置
                    board_rect.left = event.pos[0]  # 将鼠标的x坐标给Rect对象的左边
                if event.pos[0] >= w - 186 and event.pos[0] <= w:
                    board_rect.left = w - 186
                # board_rect.top = h - 17

    # 下方挡板接到小球
    if ball_y >= h - 37 and (ball_x >= board_rect.left - 20 and ball_x <= board_rect.left + 206):
        move_y = - move_y  # y方向速度反向
        score += points
        count += 1
        if count == 5:  # 每满五次，难度和单次接球得分增加
            count = 0  # 接球得分的次数清零
            points += points
            # x方向速度增加
            if move_x > 0:
                move_x += 1
            else:
                move_x -= 1
            move_y -= 1

    # 下方挡板未接到小球
    if ball_y > h - 27 and (ball_x < board_rect.left - 20 or ball_x > board_rect.left + 206):
        # 游戏结束
        ball_y = 200
        break

    # 移动小球
    ball_x += move_x
    ball_y += move_y
    if ball_x <= 20 or ball_x >= w - 20:  # 碰到左右两侧墙壁
        move_x = - move_x  # x方向速度反向
    if ball_y <= 20:  # 碰到上方墙壁
        move_y = - move_y  # y方向速度反向

    fpsClock.tick(200)
    screen.fill(color)
    # 显示分数
    my_score = font.render(str(score), False, (255, 255, 0))  # 创建文字对象（文字，是否平滑，文字颜色）
    screen.blit(my_score, (w - 100, 30))  # 将文字添加到窗口上
    screen.blit(board, board_rect)  # 将一个图像绘制在另一个图像上 把surface对象覆盖到移动后的rect对象
    pygame.draw.circle(screen, Green, (ball_x, ball_y), 20)  # 绘制小球
    pygame.display.update()  # 对显示窗口进行更新，默认窗口全部重绘
