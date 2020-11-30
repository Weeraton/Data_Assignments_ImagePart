import serial
import matplotlib.pyplot as plt
import os, sys
import numpy as np
from PIL import Image
import cv2

def listcom(l1,l2):
    if len(l1)==len(l2):
        for i in range(0,len(l1)):
            if l1[i]!=l2[i]:
                return False
    else:
        return False
    return True

def findtype(pro_img):
    #  0 0 0 0    1 1 1 1    1 x x 0    0 x x 1    x 1 1 1    x x 0 0
    #  x x x x    x x x x    1 x x 0    0 x x 1    x x 1 1    1 x x 0
    #  x x x x    x x x x    1 x x 0    0 x x 1    0 x x 1    1 1 x x
    #  1 1 1 1    0 0 0 0    1 x x 0    0 x x 1    0 0 x x    1 1 1 x
    #  bottom      top        left       right      upper      lower
    b =[0,0,0,0,1,1,1,1]
    t =[1,1,1,1,0,0,0,0]
    l =[1,0,1,0,1,0,1,0]
    r =[0,1,0,1,0,1,0,1]
    up  = [1,1,1,1,1,0,1,0,0]
    low = [0,0,1,0,1,1,1,1,1]
    t_b  = []
    t_l  = []
    t_up = []
    t_low =[]
    col = 0
    for i in pro_img:
        print(i)
        row = 0
        for j in i:
            
            if(col == 0 and row == 0):
                t_b.append(j)
                t_l.append(j)
               # print('( '+str(row)+' , '+str(col)+' )',end=' ')
            if(col == 0 and row == 1):
                t_b.append(j)
                t_up.append(j)
            if(col == 0 and row == 2):
                t_b.append(j)
                t_up.append(j)
                t_low.append(j)
            if(col == 0 and row == 3):
                t_b.append(j)
                t_l.append(j)
                t_up.append(j)
                t_low.append(j)

            if(col == 1 and row == 0):
                t_l.append(j)
                t_low.append(j)
               # print('( '+str(row)+' , '+str(col)+' )',end=' ')
            if(col == 1 and row == 2):
                t_up.append(j)
            if(col == 1 and row == 3):
                t_l.append(j)
                t_up.append(j)
                t_low.append(j)

               # print('( '+str(row)+' , '+str(col)+' )',end=' ')

            if(col == 2 and row == 0):
                t_l.append(j)
                t_up.append(j)
                t_low.append(j)
                #print('( '+str(row)+' , '+str(col)+' )',end=' ')
            if(col == 2 and row == 1):
                t_low.append(j)
            if(col == 2 and row == 3):
                t_l.append(j)
                t_up.append(j)
               # print('( '+str(row)+' , '+str(col)+' )',end=' ')

            if(col == 3 and row == 0):
                t_b.append(j)
                t_l.append(j)
                t_up.append(j)
                t_low.append(j)
            if(col == 3 and row == 1):
                t_b.append(j)
                t_up.append(j)
                t_low.append(j)
            if(col == 3 and row == 2):
                t_b.append(j)
                t_low.append(j)
            if(col == 3 and row == 3):
                t_l.append(j)
                t_b.append(j)
            #print(j,end=' ')
            
            row = row+1
        #print()
        col= col+1
    #print(up)
    #print(t_up)
    if listcom(up,t_up):
        print("Lower")
        return 5
    elif listcom(low,t_low):
        print("Upper")
        return 4
    elif listcom(r,t_l):
        print("Left")
        return 2
    elif listcom(l,t_l):
        print("Right")
        return 3
    elif listcom(t,t_b):
        print("Buttom")
        return 0
    elif listcom(b,t_b):
        print("Top")
        return 1
    else :
        print("unknow")
        return 6

def img_process(img):
    _, threshold = cv2.threshold(img,60,255,cv2.THRESH_BINARY)
    row = 0
    process_img = []
    temp1 = 0
    temp2 = 0
    temp3 = 0
    temp4 = 0
    for i in threshold:
        row+=1
        colum = 0
        for j in i:
            colum+=1
            if(j == 255):
                if(colum <=60):
                    temp1+=1
                elif(colum <=120):
                    temp2+=1
                elif(colum <=180):
                    temp3+=1
                else:
                    temp4+=1
        if((row)%80==0):
            temp1 = 1 if temp1 <3000 else 0
            temp2 = 1 if temp2 <3000 else 0
            temp3 = 1 if temp3 <3000 else 0
            temp4 = 1 if temp4 <3000 else 0
            temp=[temp1,temp2,temp3,temp4]
            process_img.append(temp)
            temp1 = 0
            temp2 = 0
            temp3 = 0
            temp4 = 0
    #send img 
    return findtype(process_img)

def collecsample(img):
    row = 0
    sixteenpoint = []
    for i in img:
        temp =[]
        row+=1
        colum = 0
        for j in i:
            colum+=1
            if((colum-30)%60==0):
                temp.append(j)
        if((row-40)%80==0):
            sixteenpoint.append(temp)
    return sixteenpoint

def capture():
    isdone = 6
    while isdone == 6:
            picn = 0
            np_img = []
            m=0
            img = []
            while(m<5):                 #Wait for start
                x = ser.read()
                if(x==b'*' and m == 0):
                    m+=1
                if(x==b'R' and m == 1):
                    m+=1
                if(x==b'D' and m == 2):
                    m+=1
                if(x==b'Y' and m == 3):
                    m+=1
                if(x==b'*' and m == 4):
                    m+=1
            for j in range(0, 240):
                temp = []
                for i in range(0,320):
                    x = ser.read()
                    z = 0
                    for l in x:
                        temp.append(l)
                img.append(temp)
            #print(img)
            np_img = np.array(img)
            im = Image.fromarray(np.uint8(np_img))
            im = im.rotate(270,expand=True)
            print("Genrate")
            #im.show(command='fim')
            astr = str(picn)+'.bmp'
            im.save(astr)
            print(astr+"save")
            img2 = cv2.imread(astr,0)
            if img2 is not None:
                    isdone = img_process(img2)
    return isdone

def capture2():
    isdone = 6
    while isdone == 6:
            picn = 0
            np_img = []
            m=0
            img = []
            while(m<5):                 #Wait for start
                x = ser.read()
                if(x==b'*' and m == 0):
                    m+=1
                if(x==b'R' and m == 1):
                    m+=1
                if(x==b'D' and m == 2):
                    m+=1
                if(x==b'Y' and m == 3):
                    m+=1
                if(x==b'*' and m == 4):
                    m+=1
            for j in range(0, 240):
                temp = []
                for i in range(0,320):
                    x = ser.read()
                    z = 0
                    for l in x:
                        temp.append(l)
                img.append(temp)
            #print(img)
            np_img = np.array(img)
            im = Image.fromarray(np.uint8(np_img))
            im = im.rotate(270,expand=True)
            print("Genrate")
            #im.show(command='fim')
            astr = str(picn)+'.bmp'
            im.save(astr)
            print(astr+"save")
            img2 = cv2.imread(astr,0)
            if img2 is not None:
                    isdone = img_process(img2)
    return collecsample(img2)

ser = serial.Serial(
        port='COM2',
        baudrate=1000000,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
servo = serial.Serial(
        port='COM10',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
C2 = serial.Serial(
        port='COM12',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
ser.flush()
servo.flush()
C2.flush()
while(1):
    print("Wait for Command")
    inp = C2.read()
    #inp = input()
    print(inp)
    send = []
    mode = 0
    if inp == b's':
        mode =1
        servo.write(b'l')
        send.append(capture())
        print("capture")
        servo.write(b'm')
        send.append(capture())
        print("capture")
        servo.write(b'r')
        send.append(capture())
        print("capture")
    if inp == b'r':
        mode =2
        servo.write(b'r')
        send = capture2()
        print("capture")
    if inp == b'l':
        mode =2
        servo.write(b'l')
        send =capture2()
        capture2()
        print("capture")
    if inp == b'c':
        mode =2
        servo.write(b'm')
        send =capture2()
        print("capture")
    s_data = 0

    if mode ==1:
        for i in send:
            s_data*=8
            s_data+=i
        print((int(s_data/256)),end=' ')
        print(bin(int(s_data/256)))
        packet = bytearray()
        packet.append(int(s_data/256))
        print(packet)
        C2.write(packet)
        print((int(s_data%256)),end=' ')
        print(bin(s_data%256))
        packet2 = bytearray()
        packet2.append(int(s_data%256))
        print(packet2)
        C2.write(packet2)


    elif mode == 2:
        row = 30
        col =40
        for i in send :
            col=0
            print("row "+str((row-30)/60))
            for j in i:
                C2.read()
                print(bin(int(row/256)),end= ' ')
                packet = bytearray()
                packet.append(int(row/256))
                C2.write(packet)
                print(bin(row%256))
                packet2 = bytearray()
                packet2.append(int(row%256))
                C2.write(packet2)

                print(bin(int(col/256)),end= ' ')
                packet = bytearray()
                packet.append(int(col/256))
                C2.write(packet)
                print(bin(col%256))
                packet2 = bytearray()
                packet2.append(int(col%256))
                C2.write(packet2)

                print(bin(int(j/256)),end= ' ')
                packet = bytearray()
                packet.append(int(j/256))
                C2.write(packet)
                print(bin(j%256))
                packet2 = bytearray()
                packet2.append(int(j%256))
                C2.write(packet2)
                col+=80
            row+=60
    #temp_reviver = reviver_in.read()
        

ser.close()