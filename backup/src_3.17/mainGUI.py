from PySide6.QtWidgets import QApplication, QVBoxLayout, QComboBox, QLabel, QWidget, QGridLayout, QHBoxLayout, QLineEdit, QCheckBox, QPushButton,QTextEdit, QProgressBar


class CounterView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

        # 初始化刷取次数
        self.times = 0
        # 模式索引
        self.mode_index:int

        # 为按钮绑定槽函数，校验输入刷取次数值，模式索引，并修改为times，mode_index
        self.button_cmit.clicked.connect(self.check_input)
        # 测试
        self.button_cancel.clicked.connect(self.get_value)

    # 初始化调用函数
    def init_ui(self):
        self.setWindowTitle('test')
        self.setGeometry(300,300,300,300)   
        self.setFixedSize(500, 500) # 固定窗口

        # 定义上半部分子视图的自布局
        sub1 = QWidget()
            # 控件
        label_mode = QLabel('选择模式：')
        self.combox = QComboBox()
        label_loop_times = QLabel("循环次数：")
        self.line_edit = QLineEdit()
        self.combox.addItem("活动")
        self.combox.addItem("御魂")
        self.combox.addItem("觉醒")
            # 布局 - 只应用在该试图
        sub1_grid = QGridLayout()
        sub1_grid.addWidget(label_mode, 0, 0)
        sub1_grid.addWidget(self.combox, 0 ,1)
        sub1_grid.addWidget(label_loop_times, 1, 0)
        sub1_grid.addWidget(self.line_edit, 1, 1)
        # 设置布局和样式
        sub1.setLayout(sub1_grid)
        sub1.setStyleSheet('background-color: #ccc; color: black;')

        # 中部分
        sub2 = QWidget()
            # 控件
        box_1 = QCheckBox('1')
        box_2 = QCheckBox('2')
        box_3 = QCheckBox('3')
        box_4 = QCheckBox('4')
            # 布局
        sub2_grid = QGridLayout()
        sub2_grid.addWidget(box_1, 0, 0)
        sub2_grid.addWidget(box_2, 0, 1)
        sub2_grid.addWidget(box_3, 1, 0)
        sub2_grid.addWidget(box_4, 1, 1)
        sub2_grid.setSpacing(1)
        sub2_grid.setContentsMargins(0, 0, 0, 0)

        sub2.setLayout(sub2_grid)
        sub2.setStyleSheet('background-color: #ccc; color: black;')

        # 下部分
        # 按钮布局
        sub3 = QWidget()
        # 布局
        sub3_layout = QVBoxLayout()
        # 控件
        self.button_cmit = QPushButton('确定')
        self.button_cancel = QPushButton('取消执行')
        self.button_cancel.setDisabled(True)
        self.logs_text = QTextEdit()
        self.logs_text.setDisabled(True)

        # 布局添加控件
        sub3_layout.addWidget(self.button_cmit, 1)   # 平分空间
        sub3_layout.addWidget(self.button_cancel, 1)   # 平分空间
        sub3_layout.addWidget(self.logs_text, 1)
        # 再来一个进度条控件
        # 启用布局
        sub3.setLayout(sub3_layout)

        layout_main = QVBoxLayout()
        layout_main.addWidget(sub1)
        layout_main.addWidget(sub2)
        layout_main.addWidget(sub3)
        layout_main.setStretchFactor(sub1, 1)
        layout_main.setStretchFactor(sub2, 2)
        layout_main.setStretchFactor(sub3, 3)

        self.setLayout(layout_main)

    def check_input(self):
        value = self.line_edit.text()
        index = self.combox.currentIndex()  # 获取选中索引
        
        try:
            value_int = int(value)
            if value_int > 0 :
                self.times = value_int  # 获取输入值并赋值
                self.mode_index = index # 赋值索引
                self.button_cmit.setDisabled(True)  # 禁用确认按钮
                self.button_cancel.setDisabled(False) # 启用取消按钮
                self.logs_text.append("开始执行")
                return 
        except ValueError:
            self.logs_text.append(f"无效输入，错误类型 {ValueError} 。")
            return None
        
    def stop_run(self):
        pass

    # 测试
    def get_value(self):
        print(self.mode_index, self.times)


if __name__ =='__main__':
    app = QApplication([])
    view = CounterView()
    view.show()
    app.exec()