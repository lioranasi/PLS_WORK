import numpy as np 
import cv2
from operator import itemgetter
from matplotlib import pyplot as plt

def nothing(x):
    pass


def calculate_heights(bob, contours): #konturler arasi mesafe
	if len(contours) == 4: #eger gorulen obje 4 kenarliysa (4 tane kontur var ise)
		b = [] #kontur noktalarinin 4unu attigimiz array

		if bob == 0: #sagdaki ve soldaki kenar uzunluklarini bulmak icin

			for point in contours: #conturlerdeki dor
				b.append(point[0])
			b.sort(key=lambda x: x[0])
			upper = b[2:4]
			lower = b[0:2]
			upper.sort(key=lambda x: x[1])
			lower.sort(key=lambda x: x[1])

			hLeft = upper[0][0]-lower[0][0]
			hRight = upper[1][0]-lower[1][0]
			return (hLeft,hRight)

		if bob == 1:
			for point in contours:
				b.append(point[0])
			b.sort(key=lambda y: y[0])
			upper = b[2:4]
			lower = b[0:2]
			upper.sort(key=lambda y: y[1])
			lower.sort(key=lambda y: y[1])
			hUp = upper[1][1]-upper[0][1]
			hDown = lower[1][1]-lower[0][1]
			return (hUp,hDown)


	else:
		#raise ValueError('len of contours is not 4')
		print("fok mutlu")

def calculate_distance(focal, px, width):

	distance = (focal * width* 10)/ px
	return(distance)


focal_length = 35
width = 29.5



cv2.namedWindow('settings')
cap = cv2.VideoCapture(0)





cv2.createTrackbar('lower_H','settings',0,180,nothing)
cv2.createTrackbar('lower_S','settings',0,255,nothing)
cv2.createTrackbar('lower_V','settings',0,255,nothing)
cv2.createTrackbar('upper_H','settings',0,180,nothing)
cv2.createTrackbar('upper_S','settings',0,255,nothing)
cv2.createTrackbar('upper_V','settings',0,255,nothing)

cv2.setTrackbarPos('lower_H','settings',110)
cv2.setTrackbarPos('lower_S','settings',50)
cv2.setTrackbarPos('lower_V','settings',50)
cv2.setTrackbarPos('upper_H','settings',130)
cv2.setTrackbarPos('upper_S','settings',255)
cv2.setTrackbarPos('upper_V','settings',255)





while (cap.isOpened()):

	_, frame = cap.read()
	img = cv2.medianBlur(frame,5)


	lowH = cv2.getTrackbarPos('lower_H','settings')
	lowS = cv2.getTrackbarPos('lower_S','settings')
	lowV = cv2.getTrackbarPos('lower_V','settings')
	upH = cv2.getTrackbarPos('upper_H','settings')
	upS = cv2.getTrackbarPos('upper_S','settings')
	upV = cv2.getTrackbarPos('upper_V','settings')



	lowerHSV = [lowH, lowS, lowV]
	upperHSV = [upH, upS, upV]

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower = np.array(lowerHSV)
	upper = np.array(upperHSV)
	mask = cv2.inRange(hsv, lower, upper)
	res = cv2.bitwise_and(frame,frame, mask= mask)

	


	contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	cnt = contours[0]



	index = 0

	for i in range (1, len(contours)):
		area = cv2.contourArea(contours[i])
		if area > cv2.contourArea(cnt):
			cnt = contours[i]
			index = i


	#print(index)

	epsilon = 0.1*cv2.arcLength(cnt,True)
	approx = cv2.approxPolyDP(cnt,epsilon,True)

	if len(contours) == 4:

		heights = calculate_heights(1, approx)



		cv2.drawContours(mask, approx, -1, (255,255,255), 5)

		distance1 =  calculate_distance(focal_length, heights[0], width)
		distance2 =  calculate_distance(focal_length, heights[1], width)

		#cv2.imshow("bob", mask)
		#print(distance1)
		
		#print(distance2)




	else:
		print("sekmiis")
		#print (heights)
		#print(index)


	cv2.imshow('video', mask)





	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
cap.release()

