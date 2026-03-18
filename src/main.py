from PySide6.QtWidgets import QApplication
from mainSRC import CounterLogic
from mainGUI import CounterView
from PySide6.QtCore import QThread
import keyboard

# 在主线程中创建对象
app = QApplication([])
view = CounterView()
logic = CounterLogic()

# 创建线程信息
thread_logic = QThread()
logic.moveToThread(thread_logic)

# 从界面获取信息，传入logic
view.sendTimes.connect(logic.setTimess)
view.sendModeIndex.connect(logic.setMod)
# 将logic处理的日志信息打印到界面
logic.Msg.connect(view.append_log)

view.startFlag.connect(logic.start) # logic.start 是阻塞线程无法执行其他信号
# view.button_cancel.clicked.connect(logic.__on_q_press)   # 进入等待时不执行, ?????为什么前面的会执行？
'''
因为logic.__on_q_press()被阻塞，不能通过信号调用，所以再在其头上封装一个函数，在该函数内直接调用，而该函数可以被信号调用，所以实现
'''
def exit_start():
    logic.__on_q_press()
view.button_cancel.clicked.connect(exit_start)

thread_logic.finished.connect(logic.deleteLater)

thread_logic.start()
# 测试可用性，为什么按钮不会禁用

def on_quit():
    thread_logic.quit()

view.show()
app.aboutToQuit.connect(on_quit)    # 退出后执行清理工作
app.exec()