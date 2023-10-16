import matplotlib.pyplot as plt

class CircleDrawer:
    def __init__(self, width, height):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-0.5*width, 0.5*width)
        self.ax.set_ylim(-0.5*height, 0.5*height)
        self.circles = []
        self.current_circle = None
        self.dragging = False
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
    
    def on_press(self, event):
        if event.button == 1:  # 左键按下
            if self.dragging:
                return
            self.current_circle = {'center': (event.xdata, event.ydata), 'radius': None}
            self.dragging = True
    
    def on_motion(self, event):
        if not self.dragging:
            return
        if event.button == 1:  # 左键拖动
            if self.current_circle['radius'] is not None:
                self.current_circle['radius'].remove()
            radius = ((event.xdata - self.current_circle['center'][0]) ** 2 + (event.ydata - self.current_circle['center'][1]) ** 2) ** 0.5
            self.current_circle['radius'] = plt.Circle(self.current_circle['center'], radius, fill=False)
            self.ax.add_artist(self.current_circle['radius'])
            self.fig.canvas.draw()
    
    def on_release(self, event):
        if event.button == 1:  # 左键释放
            if self.dragging:
                self.circles.append(self.current_circle)
                self.dragging = False
        elif event.button == 3:  # 右键按下
            if self.dragging:
                if self.current_circle['radius'] is not None:
                    self.current_circle['radius'].remove()
                self.dragging = False
    
    def on_key_press(self, event):
        if event.key == 'escape':  # 按下 Esc 键退出程序
            plt.close(self.fig)
    
    def get_circles(self):
        circles_data = []
        for circle in self.circles:
            center = circle['center']
            radius = circle['radius'].get_radius()
            circles_data.append((center[0], center[1], radius))
        return circles_data

    
    def show(self):
        plt.axis('scaled')
        plt.show()


# # 从用户输入获取二维平面的长宽
# width = int(input("请输入二维平面的宽度："))
# height = int(input("请输入二维平面的高度："))

# # 创建圆形绘制器对象
# circle_drawer = CircleDrawer(width, height)

# # 显示绘制器
# circle_drawer.show()

# # 获取圆的列表
# circles = circle_drawer.get_circles()

# # 输出圆的列表
# for circle in circles:
#     center = circle['center']
#     radius = circle['radius'].get_radius()
#     print("圆心坐标：({}, {})".format(center[0], center[1]))
#     print("半径：{}".format(radius))
