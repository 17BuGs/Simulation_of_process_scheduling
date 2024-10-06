import pygame
from pygame.locals import *
import PySimpleGUI as sg
import sys
import random
from PCB import PCB
from PCBQueue import PCBQueue
from file_reader import read_file
from process_schedule import *


class ProcessForm:
    # 定义颜色
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (200, 200, 200)
    BLACK_TRANS = (0, 0, 0, 100)
    WHITE_TRANS = (255, 255, 255, 117)
    GREEN_TRANS = (0, 255, 0, 100)
    RED_TRANS = (255, 0, 0, 100)
    BLUE_TRANS = (0, 0, 255, 100)
    GRAY_TRANS = (200, 200, 200, 100)
    LILAC = (234, 198, 255)
    LILAC_TRANS = (234, 198, 255, 200)
    PINK = (252, 186, 203)
    PINK_TRANS = (252, 186, 203, 200)

    def __init__(self, ready_queue=None, block_queue=None):
        """
        初始化函数，创建一个ProcessForm实例

        Args:
        ready_queue: 就绪队列
        block_queue: 阻塞队列
        """
        self.pcb = None
        self.sys_state = 'init'  # init, running, reset, stop
        self.ready_queue = ready_queue
        self.ready_start_pos_ptr = (230, 45)
        self.block_queue = block_queue
        self.block_start_pos_ptr = (30, 45)
        self.running_pos_ptr = (520, 50)
        self.finish_pos_ptr1 = (430, 525)
        self.finish_pos_ptr2 = (610, 525)
        self.finish_list = []  # 存储已经终止的进程
        # 设置时钟和帧率
        self.clock = pygame.time.Clock()
        self.fps = 30
        pygame.init()
        # 起始时间
        self.start_time = pygame.time.get_ticks()
        # 设置窗体尺寸
        self.size = (1050, 600)
        self.screen = pygame.display.set_mode(self.size)
        # 加载背景图片
        ori_background = pygame.image.load("bgImage.jpeg")
        # 使用 pygame.transform.scale() 函数缩小图片
        self.background = pygame.transform.scale(ori_background, self.size)
        # 加载个人图片
        ori_image = pygame.image.load('bug17.png')
        image = pygame.transform.scale(ori_image, (130, 130))
        self.image = image.convert_alpha()
        self.image_pos = (850, 100)

        # 设置标题
        pygame.display.set_caption("Process Scheduling")

        # 设置图标
        pygame.display.set_icon(pygame.image.load('bug17.ico'))

        # 创建字体对象
        self.font1 = pygame.font.SysFont("consolas", 22)  # start、reset按钮
        self.font2 = pygame.font.SysFont("consolas", 22)  # 分区标题，running pcb信息
        self.font3 = pygame.font.SysFont("consolas", 14)  # 个人信息
        self.font4 = pygame.font.SysFont("consolas", 13)  # PCB信息

        # 创建开始按钮的矩形对象
        self.start_rect = pygame.Rect(800, 490, 100, 30)
        # 创建一个Surface对象
        self.start_surface = pygame.Surface(self.start_rect.size,
                                            pygame.SRCALPHA)
        # 创建重置按钮的矩形对象
        self.reset_rect = pygame.Rect(930, 490, 100, 30)
        # 创建一个Surface对象
        self.reset_surface = pygame.Surface(self.reset_rect.size,
                                            pygame.SRCALPHA)
        # 创建继续按钮的矩形对象
        self.continue_rect = pygame.Rect(800, 530, 100, 30)
        # 创建一个Surface对象
        self.continue_surface = pygame.Surface(self.continue_rect.size,
                                               pygame.SRCALPHA)
        # 创建暂停按钮的矩形对象
        self.stop_rect = pygame.Rect(930, 530, 100, 30)
        # 创建一个Surface对象
        self.stop_surface = pygame.Surface(self.stop_rect.size,
                                           pygame.SRCALPHA)
        # 创建调度策略单选框的矩形对象
        self.sche_rect = pygame.Rect(800, 290, 230, 180)
        # 创建一个Surface对象
        self.sche_surface = pygame.Surface(self.sche_rect.size,
                                           pygame.SRCALPHA)
        # # 设置矩形框的颜色和透明度
        # self.sche_color = self.WHITE_TRANS
        # self.sche_surface.fill(self.sche_color)
        # 创建阻塞队列分区的矩形
        self.block_rect = pygame.Rect(20, 40, 180, 520)
        # 创建一个Surface对象
        self.block_surface = pygame.Surface(self.block_rect.size,
                                            pygame.SRCALPHA)
        # 设置矩形框的颜色和透明度
        self.block_color = self.RED_TRANS
        self.block_surface.fill(self.block_color)
        # 创建就绪队列分区的矩形
        self.ready_rect = pygame.Rect(220, 40, 180, 520)
        # 创建一个Surface对象
        self.ready_surface = pygame.Surface(self.ready_rect.size,
                                            pygame.SRCALPHA)
        # 设置矩形框的颜色和透明度
        self.ready_color = self.GREEN_TRANS
        self.ready_surface.fill(self.ready_color)
        # 创建执行状态分区的矩形
        self.running_rect = pygame.Rect(420, 40, 360, 50)
        # 创建一个Surface对象
        self.running_surface = pygame.Surface(self.running_rect.size,
                                              pygame.SRCALPHA)
        # 设置矩形框的颜色和透明度
        self.running_color = self.BLUE_TRANS
        self.running_surface.fill(self.running_color)
        # 创建已完成分区的矩形
        self.finished_rect = pygame.Rect(420, 135, 360, 425)
        # 创建一个Surface对象
        self.finished_surface = pygame.Surface(self.finished_rect.size,
                                               pygame.SRCALPHA)
        # 设置矩形框的颜色和透明度
        self.finished_color = self.BLACK_TRANS
        self.finished_surface.fill(self.finished_color)
        # 定义系统时间
        self.sys_time = 0
        # 创建系统时间分区的矩形
        self.time_rect = pygame.Rect(800, 40, 230, 40)
        # 创建一个Surface对象
        self.time_surface = pygame.Surface(self.time_rect.size,
                                           pygame.SRCALPHA)
        # 设置矩形框的颜色和透明度
        self.time_color = self.WHITE_TRANS
        self.time_surface.fill(self.time_color)

        # 单选框的状态
        self.selected_option = None

        # 单选框选项
        self.options = [
            "first_come_first_served", "round_robin", "shortest_process_first",
            "highest_response_ratio", "static_priority",
            "static_priority_preemptive", "dynamic_priority",
            "dynamic_priority_preemptive"
        ]

    # 用于绘制单选框的函数
    def draw_radio_button(self, x, y, option):
        """
        绘制单选框
        Args:
        x: 单选框的横坐标
        y: 单选框的纵坐标
        option: 单选框选项
        """
        # 绘制单选框的外圆
        pygame.draw.circle(self.screen, self.BLACK, (x + 5, y + 10), 8)
        pygame.draw.circle(self.screen, self.WHITE, (x + 5, y + 10), 7)

        # 绘制选中状态的内圆
        if self.selected_option == option:
            pygame.draw.circle(self.screen, self.BLACK, (x + 5, y + 10), 3)

        # 绘制选项文本
        font = pygame.font.SysFont('Comic Sans MS', 14)
        text = font.render(option, True, self.BLACK)
        self.screen.blit(text, (x + 20, y))

    def process_scheduling(self):
        """
        进程调度函数，控制系统的运行和界面的更新
        """
        # 主循环
        while True:
            # 清屏
            self.screen.fill(self.WHITE)
            self.screen.blit(self.background, (0, 0))

            # 获取鼠标位置
            mouse_pos = pygame.mouse.get_pos()

            # 判断鼠标是否在按钮上
            if self.start_rect.collidepoint(mouse_pos):
                start_color = self.GRAY_TRANS
            else:
                start_color = self.WHITE_TRANS
            # 当系统状态为running或stop时，固定按钮颜色为灰色
            if self.sys_state == 'running' or self.sys_state == 'stop':
                start_color = self.GRAY_TRANS
            self.start_surface.fill(start_color)

            # 绘制按钮
            self.screen.blit(self.start_surface, self.start_rect)

            # 绘制按钮文本
            start_text = self.font1.render("START", True, self.BLACK)
            start_text_rect = start_text.get_rect(
                center=self.start_rect.center)
            self.screen.blit(start_text, start_text_rect)

            # 判断鼠标是否在按钮上
            if self.reset_rect.collidepoint(mouse_pos):
                reset_color = self.GRAY_TRANS
            else:
                reset_color = self.WHITE_TRANS
            self.reset_surface.fill(reset_color)

            # 绘制按钮
            self.screen.blit(self.reset_surface, self.reset_rect)

            # 绘制按钮文本
            reset_text = self.font1.render("RESET", True, self.BLACK)
            reset_text_rect = reset_text.get_rect(
                center=self.reset_rect.center)
            self.screen.blit(reset_text, reset_text_rect)

            # 判断鼠标是否在按钮上
            if self.continue_rect.collidepoint(mouse_pos):
                continue_color = self.GRAY_TRANS
            else:
                continue_color = self.WHITE_TRANS
            # 当系统状态为running、init或reset时，固定按钮颜色为灰色
            if self.sys_state == 'running' or self.sys_state == 'init' or self.sys_state == 'reset':
                continue_color = self.GRAY_TRANS
            self.continue_surface.fill(continue_color)

            # 绘制按钮
            self.screen.blit(self.continue_surface, self.continue_rect)

            # 绘制按钮文本
            continue_text = self.font1.render("CONTINUE", True, self.BLACK)
            continue_text_rect = continue_text.get_rect(
                center=self.continue_rect.center)
            self.screen.blit(continue_text, continue_text_rect)

            # 判断鼠标是否在按钮上
            if self.stop_rect.collidepoint(mouse_pos):
                stop_color = self.GRAY_TRANS
            else:
                stop_color = self.WHITE_TRANS
            # 当系统状态为init、stop或reset时，固定按钮颜色为灰色
            if self.sys_state == 'init' or self.sys_state == 'stop' or self.sys_state == 'reset':
                stop_color = self.GRAY_TRANS
            self.stop_surface.fill(stop_color)

            # 绘制按钮
            self.screen.blit(self.stop_surface, self.stop_rect)

            # 绘制按钮文本
            stop_text = self.font1.render("STOP", True, self.BLACK)
            stop_text_rect = stop_text.get_rect(center=self.stop_rect.center)
            self.screen.blit(stop_text, stop_text_rect)

            # 绘制调度策略单选区域矩形
            # 如果当前系统状态为running，改变矩形颜色为灰色，表示不能更改策略
            if self.sys_state == 'running' or self.sys_state == 'stop':
                # 设置矩形框的颜色和透明度
                self.sche_color = self.GRAY_TRANS
            else:
                self.sche_color = self.WHITE_TRANS
            self.sche_surface.fill(self.sche_color)
            self.screen.blit(self.sche_surface, self.sche_rect)

            # 绘制阻塞队列分区矩形
            self.screen.blit(self.block_surface, self.block_rect)
            # 设置文字的位置和大小
            block_text = self.font2.render("Blocked Queue", True, self.BLACK)
            block_text_rect = block_text.get_rect()
            block_text_rect.topleft = (self.block_rect.left,
                                       self.block_rect.top - 22)
            self.screen.blit(block_text, block_text_rect)

            # 绘制就绪队列分区矩形
            self.screen.blit(self.ready_surface, self.ready_rect)
            # 设置文字的位置和大小
            ready_text = self.font2.render("Ready Queue", True, self.BLACK)
            ready_text_rect = ready_text.get_rect()
            ready_text_rect.topleft = (self.ready_rect.left,
                                       self.ready_rect.top - 22)
            self.screen.blit(ready_text, ready_text_rect)

            # 绘制执行状态分区矩形
            self.screen.blit(self.running_surface, self.running_rect)
            # 设置文字的位置和大小
            running_text = self.font2.render("Running Process", True,
                                             self.BLACK)
            running_text_rect = running_text.get_rect()
            running_text_rect.topleft = (self.running_rect.left,
                                         self.running_rect.top - 22)
            self.screen.blit(running_text, running_text_rect)

            # 绘制完成进程分区矩形
            self.screen.blit(self.finished_surface, self.finished_rect)
            # 设置文字的位置和大小
            finished_text = self.font2.render("Finished Process", True,
                                              self.BLACK)
            finished_text_rect = finished_text.get_rect()
            finished_text_rect.topleft = (self.finished_rect.left,
                                          self.finished_rect.top - 22)
            self.screen.blit(finished_text, finished_text_rect)

            # 绘制系统时间分区矩形
            self.screen.blit(self.time_surface, self.time_rect)
            # 设置文字的位置和大小
            time_text = self.font2.render(str(self.sys_time), True, self.BLACK)
            time_text_rect = time_text.get_rect(center=self.time_rect.center)
            self.screen.blit(time_text, time_text_rect)
            time_title_text = self.font2.render("System Time", True,
                                                self.BLACK)
            time_title_text_rect = time_title_text.get_rect()
            time_title_text_rect.topleft = (self.time_rect.left,
                                            self.time_rect.top - 22)
            self.screen.blit(time_title_text, time_title_text_rect)

            # 在窗口上绘制图片
            self.screen.blit(self.image, self.image_pos)

            # 设置个人信息文字的位置和大小
            info_text = self.font3.render("Made by BuG_17, 20213001707", True,
                                          self.BLACK)
            info_text_rect = info_text.get_rect(center=(915, 260))
            self.screen.blit(info_text, info_text_rect)

            for event in pygame.event.get():
                # 处理鼠标点击事件
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        # 检查鼠标点击位置是否在单选框范围内
                        # 当系统为running状态时，不能更改调度策略
                        if self.sys_state != 'running' and self.sys_state != 'stop':
                            for i, option in enumerate(self.options):
                                if i <= len(self.options) - 1:
                                    x, y = 810, 300 + i * 20
                                    if pygame.Rect(x, y, 200, 20).collidepoint(
                                            pygame.mouse.get_pos()):
                                        self.selected_option = option

                        # 检查鼠标点击位置是否在start按钮上
                        # 当系统为running状态时，点击无效
                        if self.sys_state != 'running' and self.sys_state != 'stop':
                            if self.start_rect.collidepoint(
                                    pygame.mouse.get_pos()):
                                self.sys_start()

                        # 检查鼠标点击位置是否在reset按钮上
                        if self.reset_rect.collidepoint(
                                pygame.mouse.get_pos()):
                            self.sys_reset()

                        # 检查鼠标点击位置是否在continue按钮上
                        if self.sys_state != 'running' and self.sys_state != 'init' and self.sys_state != 'reset':
                            if self.continue_rect.collidepoint(
                                    pygame.mouse.get_pos()):
                                # 重置本秒CPU起始时间
                                self.start_time = pygame.time.get_ticks()
                                self.sys_state = 'running'

                        # 检查鼠标点击位置是否在stop按钮上
                        if self.sys_state != 'init' and self.sys_state != 'stop' and self.sys_state != 'reset':
                            if self.stop_rect.collidepoint(
                                    pygame.mouse.get_pos()):
                                self.sys_state = 'stop'

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # 绘制单选框
            for i, option in enumerate(self.options):
                x, y = 810, 300 + i * 20
                self.draw_radio_button(x, y, option)

            # 更新时间，并更新所有PCB的状态
            if self.sys_state == 'running':
                self.update_systime()

            # 加入就绪队列
            self.join_ready(self.ready_queue)
            # 加入阻塞队列
            self.join_block(self.block_queue)
            # 加入完成的进程
            self.join_finished(self.finish_list)

            # 设置运行区pcb文本的位置和大小
            if self.pcb == None:
                running_pcb_text = "None"
            elif self.selected_option == "first_come_first_served":
                running_pcb_text = f"pid:{self.pcb.pid}-pri:{self.pcb.priority}-t:{self.pcb.running2block_time}-{self.pcb.cpu_time}/{self.pcb.all_time}"
            elif self.selected_option == "round_robin":
                running_pcb_text = f"pid:{self.pcb.pid}-pri:{self.pcb.priority}-t:{self.pcb.processing_time}/{self.pcb.time_slice}-{self.pcb.running2block_time}-{self.pcb.cpu_time}/{self.pcb.all_time}"
            elif self.selected_option == "shortest_process_first":
                running_pcb_text = f"pid:{self.pcb.pid}-pri:{self.pcb.priority}-t:{self.pcb.running2block_time}-{self.pcb.cpu_time}/{self.pcb.all_time}"
            elif self.selected_option == "highest_response_ratio":
                running_pcb_text = f"pid:{self.pcb.pid}-pri:{self.pcb.priority}-t:{self.pcb.wait_time}-{self.pcb.running2block_time}-{self.pcb.cpu_time}/{self.pcb.all_time}"
            elif self.selected_option == "static_priority":
                running_pcb_text = f"pid:{self.pcb.pid}-pri:{self.pcb.priority}-t:{self.pcb.running2block_time}-{self.pcb.cpu_time}/{self.pcb.all_time}"
            elif self.selected_option == "static_priority_preemptive":
                running_pcb_text = f"pid:{self.pcb.pid}-pri:{self.pcb.priority}-t:{self.pcb.running2block_time}-{self.pcb.cpu_time}/{self.pcb.all_time}"
            elif self.selected_option == "dynamic_priority":
                running_pcb_text = f"pid:{self.pcb.pid}-pri:{self.pcb.priority}-t:{self.pcb.running2block_time}-{self.pcb.cpu_time}/{self.pcb.all_time}"
            elif self.selected_option == "dynamic_priority_preemptive":
                running_pcb_text = f"pid:{self.pcb.pid}-pri:{self.pcb.priority}-t:{self.pcb.running2block_time}-{self.pcb.cpu_time}/{self.pcb.all_time}"

            running_pcb_text = self.font2.render(running_pcb_text, True,
                                                 self.BLACK)
            running_pcb_text_rect = running_pcb_text.get_rect(
                center=self.running_rect.center)
            self.screen.blit(running_pcb_text, running_pcb_text_rect)

            # 更新屏幕
            pygame.display.flip()

            # 控制帧率
            self.clock.tick(self.fps)

    def join_ready(self, ready_queue):
        """
        将就绪队列中的进程加入到就绪分区中

        Args:
        ready_queue: 就绪队列
        """
        cnt = 0
        curr = ready_queue.front
        while curr != None:
            cnt += 1
            pcbInfo = f"pid:{curr.pid}-pri:{curr.priority}-t:{curr.running2block_time}-{curr.cpu_time}/{curr.all_time}"
            # 创建pcb的矩形对象
            pcb_rect = pygame.Rect(230, 45 + (cnt - 1) * 35, 160, 30)
            # 创建一个Surface对象
            pcb_surface = pygame.Surface(pcb_rect.size, pygame.SRCALPHA)
            # 设置矩形框的颜色和透明度
            pcb_color = self.LILAC_TRANS
            if curr == self.pcb:
                pcb_color = self.PINK_TRANS
            pcb_surface.fill(pcb_color)
            # 绘制pcb的矩形
            self.screen.blit(pcb_surface, pcb_rect)
            # 设置文字的位置和大小
            pcb_text = self.font4.render(pcbInfo, True, self.BLACK)
            pcb_text_rect = pcb_text.get_rect(center=pcb_rect.center,
                                              left=pcb_rect.left)
            self.screen.blit(pcb_text, pcb_text_rect)
            curr = curr.next

    def join_block(self, block_queue):
        """
        将阻塞队列中的进程加入到阻塞分区中

        Args:
        block_queue: 阻塞队列
        """
        cnt = 0
        curr = block_queue.front
        while curr != None:
            cnt += 1
            pcbInfo = f"pid:{curr.pid}-pri:{curr.priority}-t:{curr.block2ready_time}-{curr.cpu_time}/{curr.all_time}"
            # 创建pcb的矩形对象
            pcb_rect = pygame.Rect(30, 45 + (cnt - 1) * 35, 160, 30)
            # 创建一个Surface对象
            pcb_surface = pygame.Surface(pcb_rect.size, pygame.SRCALPHA)
            # 设置矩形框的颜色和透明度
            pcb_color = self.LILAC_TRANS
            if curr == self.pcb:
                pcb_color = self.PINK_TRANS
            pcb_surface.fill(pcb_color)
            # 绘制pcb的矩形
            self.screen.blit(pcb_surface, pcb_rect)
            # 设置文字的位置和大小
            pcb_text = self.font4.render(pcbInfo, True, self.BLACK)
            pcb_text_rect = pcb_text.get_rect(center=pcb_rect.center,
                                              left=pcb_rect.left)
            self.screen.blit(pcb_text, pcb_text_rect)
            curr = curr.next

    def update_systime(self):
        """
        更新系统时间，并调用更新PCB状态的函数
        """
        # 计算过去的时间
        elapsed_time = pygame.time.get_ticks() - self.start_time
        # 每1.5秒更新一次数字(CPU时间+1)
        if elapsed_time >= 1500:
            self.sys_time += 1
            self.start_time = pygame.time.get_ticks()
            self.update_PCB()
            self.print_PCB_info()

    def init_queue(self):
        """
        重新读取PCB就绪队列、阻塞队列和结束的进程
        """
        self.ready_queue = read_file('ready_queue.txt', type='ready')
        self.ready_queue.display()
        self.block_queue = read_file('block_queue.txt', type='block')
        self.block_queue.display()
        self.finish_list = []

    def update_PCB(self):
        """
        根据调度策略更新PCB的状态
        """
        # 更新阻塞队列
        # 剩余阻塞时间-1
        self.block_queue.minus_blocked_time()

        # 如果策略是HRRN，等待时间+1
        if self.selected_option == "highest_response_ratio":
            self.block_queue.add_wait_time()

        if self.selected_option == "first_come_first_served":
            self.pcb = first_come_first_served(self.ready_queue, self.pcb)
            # 更新因系统资源不足而进入阻塞状态的进程块
            if self.pcb != None:
                if self.pcb.state == 'BLOCKED':
                    self.pcb.block2ready_time = random.randint(1, 10)
                    self.ready_queue.dequeue()
                    self.block_queue.enqueue(self.pcb)
                if self.pcb.state == 'FINISHED':
                    self.finish_list.append(self.pcb)

        elif self.selected_option == "round_robin":
            self.pcb = round_robin(self.ready_queue, 3)
            # 更新因系统资源不足而进入阻塞状态的进程块
            if self.pcb != None:
                if self.pcb.state == 'BLOCKED':
                    self.pcb.block2ready_time = random.randint(1, 10)
                    # 重置进程所消耗的时间片
                    self.pcb.processing_time = 0
                    self.ready_queue.del_PCB(self.pcb)
                    self.block_queue.enqueue(self.pcb)
                if self.pcb.state == 'FINISHED':
                    self.finish_list.append(self.pcb)

        elif self.selected_option == "shortest_process_first":
            self.pcb = shortest_process_first(self.ready_queue, self.pcb)
            # 更新因系统资源不足而进入阻塞状态的进程块
            if self.pcb != None:
                if self.pcb.state == 'BLOCKED':
                    self.pcb.block2ready_time = random.randint(1, 10)
                    self.ready_queue.del_PCB(self.pcb)
                    self.block_queue.enqueue(self.pcb)
                if self.pcb.state == 'FINISHED':
                    self.finish_list.append(self.pcb)

        elif self.selected_option == "highest_response_ratio":
            self.pcb = highest_response_ratio(self.ready_queue, self.pcb)
            # 更新因系统资源不足而进入阻塞状态的进程块
            if self.pcb != None:
                if self.pcb.state == 'BLOCKED':
                    self.pcb.block2ready_time = random.randint(1, 10)
                    self.ready_queue.del_PCB(self.pcb)
                    self.block_queue.enqueue(self.pcb)
                if self.pcb.state == 'FINISHED':
                    self.finish_list.append(self.pcb)

        elif self.selected_option == "static_priority":
            self.pcb = static_priority(self.ready_queue, self.pcb)
            # 更新因系统资源不足而进入阻塞状态的进程块
            if self.pcb != None:
                if self.pcb.state == 'BLOCKED':
                    self.pcb.block2ready_time = random.randint(1, 10)
                    self.ready_queue.del_PCB(self.pcb)
                    self.block_queue.enqueue(self.pcb)
                if self.pcb.state == 'FINISHED':
                    self.finish_list.append(self.pcb)

        elif self.selected_option == "static_priority_preemptive":
            # 重置上一个pcb状态（不阻塞或结束时）
            if self.pcb != None and self.pcb.state == 'RUNNING':
                self.pcb.state = 'READY'
            self.pcb = static_priority_preemptive(self.ready_queue, self.pcb)
            # 更新因系统资源不足而进入阻塞状态的进程块
            if self.pcb != None:
                if self.pcb.state == 'BLOCKED':
                    self.pcb.block2ready_time = random.randint(1, 10)
                    self.ready_queue.del_PCB(self.pcb)
                    self.block_queue.enqueue(self.pcb)
                if self.pcb.state == 'FINISHED':
                    self.finish_list.append(self.pcb)

        elif self.selected_option == "dynamic_priority":
            self.pcb = dynamic_priority(self.ready_queue, self.pcb)
            # 更新因系统资源不足而进入阻塞状态的进程块
            if self.pcb != None:
                if self.pcb.state == 'BLOCKED':
                    self.pcb.block2ready_time = random.randint(1, 10)
                    self.ready_queue.del_PCB(self.pcb)
                    self.block_queue.enqueue(self.pcb)
                if self.pcb.state == 'FINISHED':
                    self.finish_list.append(self.pcb)

        elif self.selected_option == "dynamic_priority_preemptive":
            # 重置上一个pcb状态（不阻塞或结束时）
            if self.pcb != None and self.pcb.state == 'RUNNING':
                self.pcb.state = 'READY'
            self.pcb = dynamic_priority_preemptive(self.ready_queue, self.pcb)
            # 更新因系统资源不足而进入阻塞状态的进程块
            if self.pcb != None:
                if self.pcb.state == 'BLOCKED':
                    self.pcb.block2ready_time = random.randint(1, 10)
                    self.ready_queue.del_PCB(self.pcb)
                    self.block_queue.enqueue(self.pcb)
                if self.pcb.state == 'FINISHED':
                    self.finish_list.append(self.pcb)

        else:
            # 警告弹窗中显示的文字
            message_text = "No Process Scheduling Approach Chosen!"
            # 对话框主题
            sg.theme('LightBlue')
            # 对话框布局
            layout = [[sg.Text(message_text)],
                      [sg.Button('OK', size=(6, 1), pad=((100, 0), (15, 0)))]
                      ]  # 将按钮设置为指定大小并添加边距以调整位置
            # 显示对话框
            window = sg.Window('Warning', layout, icon='bug17.ico')
            # 阻塞进程
            event, values = window.read()
            window.close()
            self.sys_reset()

        if self.sys_state == 'running':
            curr = self.block_queue.front
            while curr:
                if curr.block2ready_time <= 0:
                    curr.state = 'READY'
                    curr.running2block_time = random.randint(1, 10)
                    self.block_queue.del_PCB(curr)
                    self.ready_queue.enqueue(curr)
                curr = curr.next

    def sys_start(self):
        """
        开始运行系统，将系统状态设置为'running'
        """
        self.sys_state = 'running'
        # 重置开始计时的时间
        self.start_time = pygame.time.get_ticks()

    def sys_reset(self):
        """
        重置系统，将系统状态设置为'reset'，重置系统时间，就绪队列、阻塞队列和已完成的进程
        """
        self.sys_state = 'reset'
        # 重置系统时间
        self.sys_time = 0
        # 重置就绪队列、阻塞队列和已完成的进程
        self.init_queue()
        # 重置当前执行的进程
        self.pcb = None

    def join_finished(self, finish_list):
        """
        将已完成的进程加入已完成分区

        Args:
        finish_list: 已完成的进程列表
        """
        for i, fini_pcb in enumerate(finish_list):
            pcbInfo = f"pid: {fini_pcb.pid} - time: {fini_pcb.all_time}"
            # 创建pcb的矩形对象
            if i <= 11:
                pcb_rect = pygame.Rect(self.finish_pos_ptr1[0],
                                       self.finish_pos_ptr1[1] - i * 35, 160,
                                       30)
            else:
                pcb_rect = pygame.Rect(self.finish_pos_ptr2[0],
                                       self.finish_pos_ptr2[1] - (i - 12) * 35,
                                       160, 30)
            # 创建一个Surface对象
            pcb_surface = pygame.Surface(pcb_rect.size, pygame.SRCALPHA)
            # 设置矩形框的颜色和透明度
            pcb_color = self.LILAC_TRANS
            pcb_surface.fill(pcb_color)
            # 绘制pcb的矩形
            self.screen.blit(pcb_surface, pcb_rect)
            # 设置文字的位置和大小
            pcb_text = self.font4.render(pcbInfo, True, self.BLACK)
            pcb_text_rect = pcb_text.get_rect(center=pcb_rect.center,
                                              left=pcb_rect.left)
            self.screen.blit(pcb_text, pcb_text_rect)

    def print_PCB_info(self):
        with open(f'{self.selected_option}.txt', 'a') as file:
            file.write(f"{self.sys_time}:\n")
            file.write("running:\n")
            file.write(f"{self.pcb}\n")
            file.write("\n")
            file.write("ready queue:\n")
            temp = self.ready_queue.front
            cnt = 0
            while temp != None:
                if temp.state != 'RUNNING':
                    file.write(f"{temp}\n")
                    cnt += 1
                temp = temp.next
            if cnt == 0:
                file.write("Empty\n")
            file.write("\n")
            file.write("blocked queue:\n")
            temp = self.block_queue.front
            cnt = 0
            while temp != None:
                if temp.state != 'RUNNING':
                    file.write(f"{temp}\n")
                    cnt += 1
                temp = temp.next
            if cnt == 0:
                file.write("Empty\n")
            file.write("\n\n")
        print(f"{self.sys_time}:")
        print("running:")
        print(self.pcb)
        print()
        print("ready queue:")
        self.ready_queue.display()
        print("blocked queue:")
        self.block_queue.display()
        print()


# 主函数入口
if __name__ == '__main__':
    ready_queue = read_file('ready_queue.txt', type='ready')
    ready_queue.display()
    block_queue = read_file('block_queue.txt', type='block')
    block_queue.display()
    form = ProcessForm(ready_queue=ready_queue, block_queue=block_queue)
    form.process_scheduling()
