# # import pyautogui
# import pygetwindow as pw
# import pyautogui
# import time
# from datetime import datetime


# window:pw.Win32Window = pw.getWindowsWithTitle('阴阳师-网易游戏')[0]    # 激活窗口
# window.minimize()
# window.restore()

# window.moveTo(1, 1)
# # window.resizeTo(500, 500)
# print(window.size)

# print(window.left+20, window.right-20, window.top+window.height*0.8, window.bottom-20)
a = 20
import random
print(random.randint(2,20))

def chg():
    # global a 

    a = 100
chg()

print(a)