
import serial
import matplotlib.pyplot as plt
import os, sys
import numpy as np
from PIL import Image

def capture():
    for picn in range(0,100):
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

ser = serial.Serial(
        port='COM2',
        baudrate=1000000,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
reviver_in = serial.Serial(
        port='COM9',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
ser.flush()
reviver_in.flush()
temp_reviver = reviver_in.read()
while(1):
    temp_reviver = reviver_in.read()
    print(temp_reviver)
    if temp_reviver == b'S' :
        capture()
    
ser.close()