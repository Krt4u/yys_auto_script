import  pyautogui
import random
from time import sleep, time
import pygetwindow as pw
import json
import os
import keyboard
import atexit
from sys import maxsize
from datetime import datetime
from PySide6.QtCore import Signal, QObject
# from stdout_redirector import StdoutRedirector

class CounterLogic(QObject):

    Msg = Signal(str)

    def __init__(self):
        super().__init__()
        # self.redirector = StdoutRedirector()    ######

        self.Pause = random.randint(1, 3) / 10  # 随机库函数执行间隔
        self.lis_png_url = []
        self.dict = {}
        self.exit_flag = False
        self.times = 0   # 记录次数
        self.used_time = time()   # 记录用时
        self.start_time = 0 # 记录开始时间
        self.setTimes:int  # 设置刷取次数, 默认无限次
        self.istalk = False     # 判断该模式是否能休息是聊天
        self.width = 834
        self.height = 500
        self.setRectTimesFlag = False
        self.restartFlag = False    # 重启标志
        self.rect_times = random.randint(50, 100)   # 初始化随机休息次数
        self.steps = [pyautogui.linear,
        pyautogui.easeInQuad ,
        pyautogui.easeOutQuad ,
        pyautogui.easeInOutQuad ,
        pyautogui.easeInCubic ,
        pyautogui.easeOutCubic ,
        pyautogui.easeInOutCubic ,
        pyautogui.easeInQuart ,
        pyautogui.easeOutQuart ,
        pyautogui.easeInOutQuart ,
        pyautogui.easeInQuint ,
        pyautogui.easeOutQuint,
        pyautogui.easeInOutQuint ,
        pyautogui.easeInSine ,
        pyautogui.easeOutSine,
        pyautogui.easeInOutSine ,
        pyautogui.easeInExpo ,
        pyautogui.easeOutExpo ,
        pyautogui.easeInOutExpo  ,
        pyautogui.easeInCirc  ,
        pyautogui.easeOutCirc  ,
        pyautogui.easeInOutCirc ,
        pyautogui.easeInElastic  ,
        pyautogui.easeOutElastic ,
        pyautogui.easeInOutElastic ,
        pyautogui.easeInBack  ,
        pyautogui.easeOutBack  ,
        pyautogui.easeInOutBack  ,
        pyautogui.easeInBounce  ,
        pyautogui.easeOutBounce ,
        pyautogui.easeInOutBounce
        ]
        self.dir_path = ""
        self.timeout = 200  # 等待图片超时参数，更具部分可按需修改
        # 修改配置参数以添加副本模式
        self.mods_name = {0:'actives', 1:'soul_snake', 2:'awaking'}
        self.mods_dir = {0:'./data/actives/', 1:'./data/soul_snake/', 2:'./data/awaking'}
        pyautogui.PAUSE = self.Pause
        keyboard.add_hotkey('q+w+e', self.__on_q_press)
        keyboard.add_hotkey('q+w+r', self.__restart)

        # 将统计函数注册进入程序退出执行函数中（可注册多个函数）
        atexit.register(self.__total)

        self.origin_print = print
    
    def print(self,text):
        self.origin_print(text)
        self.Msg.emit(text)

    # 设置副本模式
    def setMod(self, target):
        self.origin_print(f"{target = }")
        if target is not None:
            self.dir_path = self.mods_dir.get(target)  # dir_path 的赋值错误会导致连锁问题
            if target != 0:
                self.origin_print(self.dir_path)
                self.istalk = True
                # 对了赋值图片路径
            else:
                self.istalk = False
        else:
            self.print('error code')
            return  # 错了直接报错返回，不获取路径

        self.__addPngToCfg()
        self.lis_png_url = self.__getUrl()

    def setTimess(self, times): # 设置刷取次数
        self.origin_print(f"{times = }")
        try:
            value = int(times)
            self.setTimes = value
            return
        except ValueError:
            self.print(f"无效输入，错误类型 {ValueError} 。")
            return
        finally:
            return
        
    # 获取副本参数
    def getModList(self):
        return self.mods_name
    
    # 写入图片路径进入配置文件
    def __addPngToCfg(self):
        dicts = {}
        for filename in os.listdir(self.dir_path):
            full_path = os.path.join(self.dir_path, filename)
            if os.path.isfile(full_path):
                name, ext = os.path.splitext(filename)
                if ext.lower() == '.png':
                    dicts[name] = full_path

        with open('./conf/config.json', 'w', encoding='utf-8') as f:
            json.dump(dicts, f)

    # 逐一获取图像url
    def __getUrl(self):
        lis = []
        with open('./conf/config.json') as f:  
            data = json.load(f)
            for key in data:
                lis.append(data[key])
        return lis

    # 获取随机曲线
    def __getStep(self):
        step = self.steps[random.randint(0, len(self.steps)-1)]
        return step

    @staticmethod
    def getWinMsg():
        window:pw.Win32Window = pw.getWindowsWithTitle('阴阳师-网易游戏')[0]
        # 获取窗口信息
        width, height = window.width, window.height
        left = window.left
        top = window.top

        posMsg = (left, top, width, height) # 识别限制区域
        return posMsg
    
    def random_move_to(self, target_x, target_y, num_points=100, duration_per_point=0.01, tween=None):
        """
        将鼠标从当前位置随机蜿蜒移动到目标点。
        :param target_x: 目标X坐标
        :param target_y: 目标Y坐标
        :param num_points: 中间随机点的数量（越多路径越曲折）
        :param duration_per_point: 每段移动的耗时（秒），总耗时 ≈ num_points * duration_per_point
        """
        # 获取当前鼠标位置
        start_x, start_y = pyautogui.position()

        # 生成随机中间点（在起点和目标点之间随机插值并添加偏移）
        points = [(start_x, start_y)]
        for _ in range(num_points):
            # 随机插值比例（0~1之间）
            t = random.uniform(0, 1)
            # 基本插值坐标
            base_x = start_x + (target_x - start_x) * t
            base_y = start_y + (target_y - start_y) * t
            # 添加随机偏移（偏移量随插值比例变化，避免超出屏幕范围）
            offset_range = int(t*50)  # 最大偏移像素
            offset_x = random.randint(-offset_range, offset_range)
            offset_y = random.randint(-offset_range, offset_range)
            # 确保坐标在屏幕范围内
            screen_width, screen_height = pyautogui.size()
            x = max(0, min(screen_width - 1, base_x + offset_x))
            y = max(0, min(screen_height - 1, base_y + offset_y))
            points.append((x, y))

        # 添加目标点作为最后一点
        points.append((target_x, target_y))

        # 去重（如果相邻点相同则跳过）
        unique_points = []
        for p in points:
            if not unique_points or p != unique_points[-1]:
                unique_points.append(p)

        # 依次移动到每个中间点
        for x, y in unique_points[1:]:  # 跳过起点（当前已在那里）
            time = random.uniform(0.1, duration_per_point)  # 随机每小步的时间
            step = self.__getStep()
            pyautogui.moveTo(x, y, duration=time, tween=step)
            # 每一个小段的值
            # print(f'per point {x ,y =}')
            # print(f'per time {time = }')
            # print(f'per step {step = }')

    def wait_for_image(self, image_path, confidence=0.8, region=None, timeout=None):
        self.print(f'waiting for {image_path}')
        if region is None:
            region = self.getWinMsg()
        if timeout is None:
            timeout = self.timeout

        start = time()
        while time() - start < timeout:
            # 退出标志检测
            # self.print("now finding")
            if self.exit_flag:
                self.print('end')
                return
            if self.restartFlag:        # 重启检测
                self.print('restart....')
                self.restartFlag = False
                return -1
                

            try:
                location = pyautogui.locateOnScreen(image_path, confidence=confidence, region=region)
                if location is not None:      # 找到图片
                    self.print("done...")
                    return location
            except pyautogui.ImageNotFoundException:
                pass                           # 没找到，继续循环
            sleep(0.5)                          # 等待0.5秒后再次检测
        return None                             # 超时返回 None

    def start(self):
        self.start_time = time()
        self.times = 0
        self.exit_flag = False

        window:pw.Win32Window = pw.getWindowsWithTitle('阴阳师-网易游戏')[0]    # 激活窗口
        window.minimize()
        window.restore()
        window.moveTo(1, 1)
        window.resizeTo(self.width, self.height)   # 勿动！
        sleep(1)

        current_times = 0   # 初始化未休息次数

        if not self.lis_png_url:    # 路径有问题，终止执行
            self.print("path error")
            return

        while 1 and self.times < self.setTimes:     # 超时退出
            if self.exit_flag:
                self.print('end')
                return
                
            if self.restartFlag:        # 重启检测
                self.print('restart....')
                self.restartFlag = False
                continue

            isFull = 0  # 完整执行标志
            for url in self.lis_png_url:
                location = self.wait_for_image(url)
                if not location:
                    self.print("图片无效，请重新检查")   # 未找到则跳过该次查找，进入下一次
                    continue
                if location == -1:  # 检测wait_for_image中的退出标志
                    break

                pos = pyautogui.center(location)
                self.origin_print(f"目标中点 {pos.x = }, {pos.y = }")  # 目标中点

                x = pos.x + random.uniform(-20,20)    # 设置按钮偏移
                y = pos.y + random.uniform(-20,20)

                # 结算时先快速点击加快加载
                # 在窗口内随机
                if url == self.lis_png_url[1] or url == self.lis_png_url[-1]:
                    x = random.uniform((window.left+window.right)/2, window.right-20) # 界面宽度范围内
                    y = random.uniform(window.top+window.height*0.75, window.bottom-20)     # 界面 4/5-1 以内高度
                    # print(f"------ -1 {x = }, {y = } ---------")
                    # 结算时移动并点击
                    # 只有两张也没问题，因为此时 1 = -1 ，不会执行下面的elif语句
                    if url == self.lis_png_url[1]:
                        self.random_move_to(x, y, random.randint(1,3), random.uniform(0, 0.1))
                        # sleep(random.randint(1, 3)/10)
                        pyautogui.click(clicks=random.randint(3,5), interval=random.uniform(0,0.1))
                        continue
                    # 结算完点击
                    elif url == self.lis_png_url[-1]:
                        sleep(random.randint(5,7)/10)  # 休眠，等稳定后再点击，问题很可能出在相同位置这里，因为第三张图片出现前游戏有停留
                        # 移动增加容错
                        self.random_move_to(x, y, random.randint(1,3), random.uniform(0, 0.1))
                        pyautogui.click(clicks=random.randint(3,5), interval=random.uniform(0.1, 0.15))
                        
                        # 当执行完最后一张图片时 [-1] ，视为完整执行
                        isFull = 1

                elif url == self.lis_png_url[0]:
                    sleep(random.randint(3,5)/10) # 随机停止
                    # 在图标内随机
                    self.random_move_to(x, y, random.randint(3,5), random.uniform(0, 0.1))
                    pyautogui.click(clicks=random.randint(2,3), interval=random.uniform(0,0.1))
                    # 移动到随机位置
                    random_x = random.uniform(window.left-20, window.right-20)
                    random_y = random.uniform(window.top+20, window.bottom-20)
                    self.random_move_to(random_x, random_y, random.randint(3,5), random.uniform(0, 0.2))

                self.origin_print(f"实际点击 {x = }, {y = }")   # 实际点击位置


            self.times+=isFull   # 记录副本总次数
            current_times+=isFull  # 记录未休息次数

            self.print(f"共已执行 {self.times} 次，总剩余 {self.setTimes-self.times} 次。上一次休息已经过 {current_times} 次，距离下一次休息 {self.rect_times - current_times} 次")
            if self.__rest(current_times): # 未休息次数是否匹配因休息次数，30 - 50次时休息
                current_times = 0   # 执行休息，未休息次数重置
                rect = random.randint(30, 60)     # 随机休息时间
                for t in range(0, rect):
                    self.print(f"执行休息，已经休息 {t}s, 剩余 {rect - t}s", flush=True)
                    sleep(1)
                if self.istalk:
                    self.print('非活动模式，进入聊天')
                    self.__talk()
                else:
                    self.print('活动模式，仅休息')

    def __rest(self, times):

        if self.setRectTimesFlag:   # 检查休息重置标志，若为（true）则上次休息次数已被匹配，重新生成一个
            self.rect_times = random.randint(50, 100)   # 重新设置值
            self.setRectTimesFlag = False   # 重新调回标志

        if times == self.rect_times:
            self.setRectTimesFlag = True    # 休息次数已经被匹配一次，更改重置休息次数标志
            return True
        return False

        

    def __talk(self):
        location_msg = self.wait_for_image('./data/rect/1msg.png') # 获取聊天位置
        pos_msg = pyautogui.center(location_msg) 
        # 设置偏移
        x = pos_msg.x+ random.uniform(-7, 7)
        y = pos_msg.y+ random.uniform(-7, 7)
        # 移动
        self.random_move_to(x, y, random.randint(1,3), random.uniform(0, 0.2))
        sleep(random.uniform(0, 1))
        pyautogui.click()    # 点击msg进入聊天

        sleep(random.randint(0,10)/10)

        # 获取输入框 并进入
        location_input = self.wait_for_image('./data/rect/input.png')  
        pos_inp = pyautogui.center(location_input)
        # 设置偏移
        x = pos_inp.x+ random.uniform(-20, 20)
        y = pos_inp.y+ random.uniform(-5, 5)
        # 移动
        self.random_move_to(x, y, random.randint(3,5), random.uniform(0, 0.2))
        sleep(random.uniform(0, 1))
        pyautogui.click()   

        sleep(random.uniform(0.5,1))

        now = datetime.now()
        pyautogui.write(now.strftime("%Y-%m-%d %H:%M:%S"), interval=0.2)    # 输入内容

        sleep(random.uniform(0.5,1))

        # 获取发送位置信息
        location_send = self.wait_for_image('./data/rect/send.png')  
        pos_send = pyautogui.center(location_send)
        # 设置偏移
        x = pos_send.x+ random.uniform(-10, 10)
        y = pos_send.y+ random.uniform(-7, 7)
        # 移动
        self.random_move_to(x, y, random.randint(3,5), random.uniform(0, 0.2))
        sleep(random.uniform(0.5, 1))
        pyautogui.click()


        sleep(0.5)
        # 设置偏移
        x = pos_msg.x+ random.uniform(-7, 7)
        y = pos_msg.y+ random.uniform(-7, 7)
        # 移动
        self.random_move_to(x, y, random.randint(1,3), random.uniform(0, 0.2))
        sleep(random.uniform(0, 1))
        pyautogui.click()    # 点击msg关闭聊天
        
    def __on_q_press(self):
        self.origin_print('cal1')
        self.exit_flag = True

    def __total(self):
        self.print(f'执行结束，共计 {self.times} 次，用时 {int(time() - self.start_time)}s ')

    def __restart(self):
        window:pw.Win32Window = pw.getWindowsWithTitle('阴阳师-网易游戏')[0]    # 激活窗口
        window.minimize()
        window.restore()
        window.moveTo(1, 1)
        window.resizeTo(self.width, self.height)   # 勿动！
        sleep(1)
        self.print('restart exec')
        self.restartFlag = True

    # def __shutdown(self):
    #     os.system('shutdown -s -t ')

def main():
    test = CounterLogic()
    test.setTimess(100)
    test.setMod(1)
    test.start()


if __name__ == '__main__':

    main()