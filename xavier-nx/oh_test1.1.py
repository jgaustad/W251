import numpy as np
import time
import cv2
# testing 
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier("opencv/data/haarcascades/haarcascade_frontalface_default.xml")

counter = 0
cadence = 100

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	print(type(gray), gray.shape)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		print('face detected', x,y,w,h)
		cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
		gray_face = gray[y:y+h, x:x+w]
		print(time.time())
		rc,png = cv2.imencode('.png', gray_face)
		msg = png.tobytes()
		if counter%10 == 0:  # only save the 10th face
			with open('images/face'+str(counter)+'.png', 'wb') as file:
				file.write(msg)
		counter += 1        
		#time.sleep(5)

	cv2.imshow('frame',gray)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
