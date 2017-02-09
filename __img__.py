import cv2
import numpy as np
import collections

cap = cv2.VideoCapture(0)
framex = 1278
framey = 718
pxl = []
clr = []
counting = []


while (1):

    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_limit = np.array([110,50,50])
    upper_limit = np.array([130,255,255])

   

    lower_limit2 = np.array([50, 110, 50])
    upper_limit2 = np.array([255, 130, 255])
    
    lower_limit3 = np.array([50, 50, 110])
    upper_limit3 = np.array([255, 255, 130])

                                                                                                                                           


    for y in range(0, framey, 7):

        pxl = []
        clr = []
        counting = []
       
        
        for x in range(0,framex, 7):
            #clr.append(x/7)
            a = frame[y, x][0] 
            b = frame[y, x][1]
            c = frame[y, x][2]
            pixel = [a, b, c] 
            if (a > 110 & a < 130 & b > 50 & b < 255 & c > 50 & c < 255 ):
                #print ("blue")   
                #print(" ")
                clr.append(1)
            

            elif (a > 50 & a < 255 & b > 110 & b < 130 & c > 50 & c < 255):
                #print("green") 
                #print(" ")  
                clr.append(2)
            
            elif (a > 50 & a < 255 & b > 50 & b < 255 & c > 110 & c < 130):
                #print("red") 
                #print(" ") 
                clr.append(3)

            else:
                #print("____________________________________________________")
                clr.append(0) 


            #pixel2 = [yaxis, xaxis, xaxis]
            pxl.append(pixel)

            

            #print(clr)

        c = collections.Counter(clr)
        #print(c)

        #for item in count in c.items: #WTF
        #d = count in collections.Counter(c).items()
            #if (count > 100):
                #print (d)

        d = [item for item, count in collections.Counter(c).items() if count > 100] 
        #print (d)
        counting.append(d)
        print (counting)


    mask_blue = cv2.inRange(hsv, lower_limit, upper_limit)
    mask_green = cv2.inRange(hsv, lower_limit2, upper_limit2)
    mask_red = cv2.inRange(hsv, lower_limit3, upper_limit3)
    mask = mask_green + mask_red + mask_blue

    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    #cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)
    cv2.imshow('res', res)
    



    #break

    

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break



cv2.destroyAllWindows()# frc_top-
# frc_top-
# frc_top-
# image_processing_frc
# image_processing_frc
