"""
Not import modi. Just write about GUI programming in this scripts. Only for testing GUI.
Author: Ryu Taehun
"""

import tkinter as tk
from math import ceil,floor
import threading as th

keep_going = True

window=tk.Tk()
window.title("Motion GUI")
window.geometry("1100x600")
window.resizable(True, True)

bottomWindow = tk.Frame(window)
bottomWindow.grid(row = 14)

# 동작 배열 관련
stack_index = 0

# 동작배열 개수 설정.
range_move = 10
move_for_stack = [[50 for i in range(12)] for j in range(range_move)]

## 초기 모터 위치. 전부 다 50이면 좋겠지만 일일이 찾아주는게 좋음.
initial_pose = [50 for i in range(12)] 

# 모터 인덱스 배열
left_index = [0,1,2,3,4,5]
right_index = [6,7,8,9,10,11]

# 전체동작실행 시 업데이트 될 예정. 
# index: 0,1 // 4,5 // 8,9
left_triangle_pose = [50 for i in range(6)]
# index: 2,3 // 6,7 // 10,11
right_triangle_pose = [50 for i in range(6)]

def select(self):
    value = [0 for i in range(12)]

    for i,j,k in zip(range(12),(1,1,2,2,3,3,4,4,5,5,6,6),(1,2,1,2,1,2,1,2,1,2,1,2)):
        value[i]= str(j)+"-"+str(k)+" 모터 값 : "+str(scale[i].get())
        label[i].config(text=value[i])

var = [tk.IntVar() for i in range(12)]
scale = [0 for i in range(12)]
label = [0 for i in range(12)]

label_set1=tk.Label(window, text="로봇 기준 왼쪽 다리")
label_set1.grid(row=0, column=0)
label_set2=tk.Label(window, text="로봇 기준 오른쪽 다리")
label_set2.grid(row=0, column=3)

for i,j,k in zip(range(12),(1,1,2,2,3,3,4,4,5,5,6,6),(1,2,1,2,1,2,1,2,1,2,1,2)):
    if i in left_index:

        scale[i]=tk.Scale(window, variable=var[i], command=select, orient="horizontal", showvalue=False, tickinterval=10, to=100, length=300, 
                                activebackground="red")
        scale[i].set(50)
        scale[i].grid(row=i*2+1,column=0)
        label[i]=tk.Label(window, text=str(j)+"-"+str(k)+" 모터 값 : 0")
        label[i].grid(row=(i+1)*2, column=0)

    elif i in right_index:

        scale[i]=tk.Scale(window, variable=var[i], command=select, orient="horizontal", showvalue=False, tickinterval=10, to=100, length=300, 
                                activebackground="blue")
        scale[i].set(50)
        scale[i].grid(row=2*(i-6)+1,column=3)
        label[i]=tk.Label(window, text=str(j)+"-"+str(k)+" 모터 값 : 0")
        label[i].grid(row=2*(i-5),column=3)

    
###################  모터 움직임 #####################
def btncmd(index):
    m_degree = scale[index].get()
    flr_index_2 = floor(index/2)
    if index <=5:
        left_triangle_pose[index] = m_degree
    else:
        right_triangle_pose[index-6] = m_degree


    print(str(flr_index_2+1)+"-"+str(ceil(index%2)+1),"모터 값",m_degree)
    print("Present Setting:",left_triangle_pose,right_triangle_pose)

def btninitalenroll():
    for i in range(12):
        initial_pose[i]=scale[i].get()
    print("Set New Initial Pose: ",initial_pose)

def btninitial():
    for i in range(12):
        scale[i].set(initial_pose[i])

    print("Move Initial Pose:",initial_pose)

def btnleft():
    for i,j in enumerate(left_index):
        left_triangle_pose[i] = scale[j].get()
    
    print("Move left Motors:",left_triangle_pose)

def btnright():
    for i,j in enumerate(right_index):
        right_triangle_pose[i] = scale[j].get()

    print("Move right Motors:",right_triangle_pose)

def btnall(): # 현재 Scale bar 설정대로 모든 모터 한번에 바꿈
    for i,j in enumerate(left_index):
        left_triangle_pose[i] = scale[j].get()

    for i,j in enumerate(right_index):
        right_triangle_pose[i] = scale[j].get()

    print("Move All",left_triangle_pose,right_triangle_pose)

def initialPosePrint():
    print("Print Initial Pose",initial_pose)

def stackvalue():
    try:
        global stack_index, move_label
        for i,j in enumerate(left_index):
            left_triangle_pose[i] = scale[j].get()

        for i,j in enumerate(right_index):
            right_triangle_pose[i] = scale[j].get()

        for i,j in enumerate((6,7,8,9,10,11)):
            move_for_stack[stack_index][i] = left_triangle_pose[i]
            move_for_stack[stack_index][j] = right_triangle_pose[i]

        move_label = tk.Label(bottomWindow, text=move_for_stack[stack_index][0:12])
        move_label.grid(row=stack_index,column=0)
        print("현재 동작 배열",move_for_stack,"\n")
        stack_index +=1
    except IndexError:
        print("--------가능한 배열 범위를 벗어났습니다.---------")

def initializeStack():
    global stack_index
    move_for_stack = [[50 for i in range(12)] for j in range(range_move)]

    mylist = bottomWindow.grid_slaves()
    for i in mylist:
        i.destroy()

    stack_index = 0
    print("동작 배열 초기화",move_for_stack)

def startStack():
    print(">>동작배열 한번 실행")

def startWhileStack():
    global keep_going
    keep_going = True

    # 키보드 잡히는지 체크
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    
    # 실제 구동 코드
    while keep_going:
        print(">>>>무한반복중...멈추려면 아무 키나 입력 후 Enter")

# 키보드 입력 확인
def key_capture_thread():
    global keep_going
    input()
    keep_going = False

#########################################################################   

btn = [None]*12
btn[0] = tk.Button(window, text="1-1 실행", command= lambda: btncmd(0))
btn[1] = tk.Button(window, text="1-2 실행", command= lambda: btncmd(1))
btn[2] = tk.Button(window, text="2-1 실행", command= lambda: btncmd(2))
btn[3] = tk.Button(window, text="2-2 실행", command= lambda: btncmd(3))
btn[4] = tk.Button(window, text="3-1 실행", command= lambda: btncmd(4))
btn[5] = tk.Button(window, text="3-2 실행", command= lambda: btncmd(5))
btn[6] = tk.Button(window, text="4-1 실행", command= lambda: btncmd(6))
btn[7] = tk.Button(window, text="4-2 실행", command= lambda: btncmd(7))
btn[8] = tk.Button(window, text="5-1 실행", command= lambda: btncmd(8))
btn[9] = tk.Button(window, text="5-2 실행", command= lambda: btncmd(9))
btn[10] = tk.Button(window, text="6-1 실행", command= lambda: btncmd(10))
btn[11] = tk.Button(window, text="6-2 실행", command= lambda: btncmd(11))

for i in range(12):
    if i in left_index:
         btn[i].grid(row=2*i+1,column=1)

    elif i in right_index:
        btn[i].grid(row=2*(i-6)+1,column=4)


btn_initial_print = tk.Button(window, text="초기모션 프린트", command=initialPosePrint)
btn_initial_print.grid(row=0,column=6)

btn_initial_enroll = tk.Button(window, text="새로운 초기모션 등록", command=btninitalenroll)
btn_initial_enroll.grid(row=1,column=6)

btn_initial = tk.Button(window, text="초기모션 실행", command=btninitial)
btn_initial.grid(row=2,column=6)

btn_left = tk.Button(window, text="left모터만 실행", command=btnleft)
btn_left.grid(row=3,column=6)

btn_right = tk.Button(window, text="right모터만 실행", command=btnright)
btn_right.grid(row=4,column=6)

btn_all = tk.Button(window, text="모든 모터 실행", command=btnall)
btn_all.grid(row=5,column=6)

btn_stack = tk.Button(window, text="동작 배열에 추가",command=stackvalue)
btn_stack.grid(row=7,column=6)

btn_stack_reset = tk.Button(window, text="동작 배열 초기화",command=initializeStack)
btn_stack_reset.grid(row=8,column=6)

btn_stack_start = tk.Button(window, text="동작 배열 1번 실행",command=startStack)
btn_stack_start.grid(row=11,column=6)

btn_stack_start = tk.Button(window, text="동작 배열 무한 반복",command=startWhileStack)
btn_stack_start.grid(row=12,column=6)

move_label_start = tk.Label(window, text="-----------모터 12개 동작 배열(L R 순). 최대"+str(range_move)+"개----------")
move_label_start.grid(row=13,column=0)


window.grid_columnconfigure(2, minsize=20)
window.grid_columnconfigure(5, minsize=40)


window.mainloop()