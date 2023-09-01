import random
import math
import matplotlib.pyplot as plt
import pandas as pd
from CircleDrawer import CircleDrawer
def generate_tangent_circles(n, x_min, x_max, y_min, y_max):
    circles = []
    
    def is_tangent(circle1, circle2):
        distance = math.sqrt((circle1[0] - circle2[0])**2 + (circle1[1] - circle2[1])**2)
        return distance <= circle1[2] + circle2[2]
    
    def is_within_bounds(circle):
        return circle[0] - circle[2] >= x_min and circle[0] + circle[2] <= x_max and \
               circle[1] - circle[2] >= y_min and circle[1] + circle[2] <= y_max
    
    def generate_circle():
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        radius = random.uniform(min(x_max - x_min, y_max - y_min) / 20, min(x_max - x_min, y_max - y_min) / 5)
        return (x, y, radius)
    
    def circles_overlap(circle):
        for existing_circle in circles:
            if is_tangent(circle, existing_circle) or not is_within_bounds(circle):
                return True
        return False
    
    interation = 0
    while len(circles) < n and interation<= 100000:
        interation +=1
        print("尝试创建圆：{}".format(len(circles)),"已经迭代次数：{}".format(interation),end = '\r')
        circle = generate_circle()
        if not circles_overlap(circle):
            circles.append(circle)
    
    return circles

def plot_circles(circles, x_min, x_max, y_min, y_max):
    plt.figure()
    ax = plt.gca()
    for circle in circles:
        ax.add_patch(plt.Circle((circle[0], circle[1]), circle[2], fill=False))
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    plt.axis('equal')
    plt.show()


def read_atom_data(data_file):
    with open(data_file, 'r') as file:
        lines = file.readlines()

    atoms_line = lines[2].split()
    num_atoms = int(atoms_line[0])

    x_range = lines[5].split()
    x_min, x_max = float(x_range[0]), float(x_range[1])
    y_range = lines[6].split()
    y_min, y_max = float(y_range[0]), float(y_range[1])
    z_range = lines[7].split()
    z_min, z_max = float(z_range[0]), float(z_range[1])

    masses_line = lines[11].split()
    atom_type = int(masses_line[0])
    atom_mass = float(masses_line[1])

    atom_lines = lines[15:15+num_atoms]
    columns = ['atom_id', 'atom_type', 'x', 'y', 'z', 'image0', 'image1', 'image2']
    data = []
    process = 0
    for line in atom_lines:
        if process%100 == 0:
            print("读取data文件中，进度：{}/{}".format(process,num_atoms),end='\r')
        process +=1
        atom_info = line.split()
        atom_id = int(atom_info[0])
        atom_type = int(atom_info[1])
        x = float(atom_info[2])
        y = float(atom_info[3])
        z = float(atom_info[4])
        image0 = int(atom_info[5])
        image1 = int(atom_info[6])
        image2 = int(atom_info[7])
        data.append([atom_id, atom_type, x, y, z, image0, image1, image2])

    df = pd.DataFrame(data, columns=columns)
    return df,x_min,x_max,y_min,y_max,z_min,z_max,atom_mass

def check_atoms_in_circles(df, circles):
    df['in_circle'] = False
    for i, row in df.iterrows():
        print("目前正在判定原子：{}".format(i),end = '\r')
        atom_x = row['x']
        atom_y = row['y']
        for circle in circles:
            circle_x = circle[0]
            circle_y = circle[1]
            circle_radius = circle[2]
            distance = (atom_x - circle_x)**2 + (atom_y - circle_y)**2
            if distance <= circle_radius**2:
                df.at[i, 'in_circle'] = True
                break

    return df[df['in_circle']]

def format_data_file(df, x_min, x_max, y_min, y_max, z_min, z_max, output_file):
    with open(output_file, 'w') as file:
        file.write("Generated data\n\n")
        file.write("\n")
        file.write(" {} atoms\n".format(len(df)))
        file.write(" 1 atom types\n")
        file.write("\n")
        file.write(" {:.3f} {:.3f} xlo xhi\n".format(x_min, x_max))
        file.write(" {:.3f} {:.3f} ylo yhi\n".format(y_min, y_max))
        file.write(" {:.3f} {:.3f} zlo zhi\n".format(z_min, z_max))
        file.write("\n")
        file.write("Masses\n")
        file.write("\n")
        file.write(" 1 {:.2f}\n".format(atom_mass))
        file.write("\n")
        file.write("Atoms # atomic\n")
        file.write("\n")
        for i, row in df.iterrows():
            atom_id = row['atom_id']
            atom_type = row['atom_type']
            x = row['x']
            y = row['y']
            z = row['z']
            image0 = row['image0']
            image1 = row['image1']
            image2 = row['image2']
            file.write(" {} {} {:.6f} {:.6f} {:.6f} {} {} {}\n".format(atom_id, atom_type, x, y, z, image0, image1, image2))
# 调用函数读取data文件并存储到DataFrame中
data_file = r'C:\codes\拖动+bubble/test1.data'  # 替换为您的data文件路径
df,x_min,x_max,y_min,y_max,z_min,z_max,atom_mass = read_atom_data(data_file)
width = x_max-x_min
height = y_max-y_min
print("数据读入完成：原子数为{}".format(df.shape[0]),"长宽为：{}//{}".format(width,height))

print("需要自动绘制或手动绘制？ 自动/手动 y/n")
select = input("请输入：")
if select == str("y"):
    # 指定xy平面的大小和生成的圆的数量
    lattice_constant =4.0479
    #x_min = -40*lattice_constant
    #x_max = 40*lattice_constant
    #y_min = -300*lattice_constant
    #y_max = 300*lattice_constant
    n = 300
    circles = generate_tangent_circles(n, x_min, x_max, y_min, y_max)
    plot_circles(circles, x_min, x_max, y_min, y_max)
else:
    if select == str("n"):
        # 创建圆形绘制器对象
        circles = []
        circle_drawer = CircleDrawer(width, height)
        # 显示绘制器
        circle_drawer.show()
        circles = circle_drawer.get_circles()
        plot_circles(circles, x_min, x_max, y_min, y_max)
    else:
        print("意外输入，程序终止！！")

print("创建的总圆数量：{}个".format(len(circles)))
# for circle in circles:
#     print("圆心坐标: ({}, {}), 半径: {}".format(circle[0], circle[1], circle[2]))

df_in_circle = check_atoms_in_circles(df, circles)

# 输出重新格式化后的data文件
output_file = r'C:\codes\拖动+bubble/output_data.data'  # 替换为输出的data文件路径
format_data_file(df_in_circle, x_min, x_max, y_min, y_max, z_min, z_max, output_file)
