import random


def fill():
    """随机寻找game中的格子，若格子中的值为0则随机填充2或4"""
    fill_in = True
    while fill_in:
        r1 = random.randint(0, 3)
        r2 = random.randint(0, 3)
        r = game[r1][r2]
        if r == 0:
            game[r1][r2] = random.choice([2, 4])
            fill_in = False


def print_game(a):
    """输出game，类似4x4的棋盘"""
    for i in a:
        print(i)


def slide(direction, a):
    """实现滑动操作，WASD分别控制上左下右滑动"""
    # 调用move()函数实现列表中的元素移动并相加，将原来的列表赋值为移动后的列表
    if direction == 'D':
        for row in range(0, ROW):
            a[row] = move(a[row])
    if direction == 'A':
        for row in range(0, ROW):
            a[row] = move(a[row][::-1])[::-1]
    # 创建一个大列表，将每一列的元素添加到小列表中，再调用move()函数实现小列表中的元素移动并相加，移动后的小列表添加到一个大列表中，
    # 再将每一个原来的元素按照一定的方式替换为大列表中的元素
    if direction == 'W':
        erect_list = []
        for col in range(0, COL):
            e_erect_list = []
            for row in range(-1, -ROW-1, -1):
                e_erect_list.append(a[row][col])
            erect_list.append(move(e_erect_list))
        for i in range(0, COL):
            for j in range(-1, -ROW-1, -1):
                a[-j-1][i] = erect_list[i][j]
    if direction == 'S':
        erect_list = []
        for col in range(0, COL):
            e_erect_list = []
            for row in range(0, ROW):
                e_erect_list.append(a[row][col])
            erect_list.append(move(e_erect_list))
        for i in range(0, COL):
            for j in range(-1, -ROW - 1, -1):
                a[j][i] = erect_list[i][j]
    return a


def move(li):
    """通过列表切片实现列表中的元素移动并相加（写个例子带入一下即可验证并理解该算法是正确的）"""
    # 指针从最右端开始（直到从左往右数第二位结束），判断指针左边的列表中的元素是否全部为0
    # (如果不进行这个判断会导致后来指针一直卡在0的地方，死循环)
    # 如果不是，则进行移动操作：
    #   将从指针到从左往右数第二位的列表切片赋值为为指针左边（不包含指针所在的位置）的列表，
    #   并将最后最左边的元素赋值为0，
    #   直到指针所在的位置的元素的值不为0为止
    for i in range(-1, -len(li), -1):
        if li[i:-len(li) - 1:-1] != [0] * (len(li) + i + 1):
            while li[i] == 0:
                li[i:-len(li):-1] = li[i - 1:-len(li) - 1:-1]
                li[0] = 0
    # 指针从最右端开始（直到从左往右数第二位结束）（for循环可保证同一个位置不会进行两次相加操作）
    # 如果指针所在的位置的元素的值和指针左边一位所在的位置的元素的值相等，则进行相加操作：
    # 将从指针到从左往右数第二位的列表切片赋值为为指针左边（不包含指针所在的位置）的列表
    # 并将最后最左边的元素赋值为0，
    # 再将指针所在的位置的元素的值变为原来的两倍
    for i in range(-1, -len(li), -1):
        if li[i] == li[i - 1]:
            li[i:-len(li):-1] = li[i - 1:-len(li) - 1:-1]
            li[0] = 0
            li[i] *= 2
    return li


def command_input():
    """正确的获取用户输入"""
    commanding = True
    while commanding:
        command = input("请输入操作：").upper()
        # 判断用户输入是否在操作字典中，如果是则结束输入
        if command in command_dic:
            commanding = False
        else:
            print("请正确输入操作！！！")
    return command


def end_game(a):
    """用于判断是否满足结束游戏的条件"""
    # 循环二维数组中的元素，记录0出现的次数，若0出现了0次，则结束游戏，若出现2048则游戏胜利（结束游戏）
    n = 0
    for row in range(ROW):
        for col in range(COL):
            if a[row][col] == 0:
                n += 1
            if a[row][col] == 2048:
                print("WIN！！！")
                return True
    if n == 0:
        print("DEFEAT!!!")
        return True
    else:
        return False


def print_information():
    """打印操作说明"""
    print("操作说明：")
    for key, value in command_dic.items():
        print(f"{key}键：{value}")
    print()


# 定义一个操作的字典，方便后续检测输入的操作是否正确和输出信息
command_dic = {"W": "向上滑动", "A": "向左滑动", "S": "向下滑动", "D": "向右滑动"}
game = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # 2048的载体为一个二维数组，0代表空格子
ROW = len(game)  # 行
COL = len(game[0])  # 列
print_information()
print("游戏开始")
# 初始化游戏，填充两个格子，并显示
fill()
fill()
print_game(game)
# 持续判断是否满足结束游戏的条件，如果不满足则实现游戏，如果满足则结束游戏
while not end_game(game):
    print_game(slide(command_input(), game))
    fill()
