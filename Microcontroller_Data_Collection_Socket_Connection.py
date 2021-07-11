import socket
import msvcrt
import csv



def kbfunc():
    #this is boolean for whether the keyboard has been hit
    x = msvcrt.kbhit()
    if x:
        #getch acquires the character encoded in binary ASCII
        ret = msvcrt.getch()
    else:
        ret = False
    return ret

l = []
packet = []
p = ""
tp = []
s = socket.socket()         
 
s.bind(('0.0.0.0', 80 ))
s.listen(0)          



record = input("Press R to start recording...")
if record == 'r' :
    
    client, addr = s.accept()
    carry = ''   
    try:
        while True:
            content = client.recv(1)
            

            if len(content) ==0:
                # print("heree?")
                break

            else:
                #print(len(content))
              
                temp = ''
                content = content.decode("utf-8")
                if content == '!':
                    
                    tp =[]
                    p = ''

                
                elif content == '@':
                    tp.append(p)
                    p = ''
                    tp.append('RA')
                    packet.append(tp)
                    print(tp)

                elif content ==',':
                    tp.append(p)
                    p = ''

                else:
                    p += content


    except KeyboardInterrupt:
        pass   
    client.close()
    print(len(packet))

    
    with open('FILE_NAME.csv','w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z","label"])
        
        writer.writerows(packet)

 
