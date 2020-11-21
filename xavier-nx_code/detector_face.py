import numpy as np
import time
import cv2
# testing 
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier("opencv/data/haarcascades/haarcascade_frontalface_default.xml")

counter = 0
cadence = 10


import paho.mqtt.client as mqtt


LOCAL_MQTT_HOST="mosquitto"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="jtopic"

def on_connect_local(client, userdata, flags, rc):
	print("connected to local broker with rc: " + str(rc))
	#client.subscribe(LOCAL_MQTT_TOPIC)

def paho_publish(msg, client):
	client.publish(LOCAL_MQTT_TOPIC, payload=msg)

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
#local_mqttclient.on_message = on_message



# go into a loop
#local_mqttclient.loop_forever()

# connect and move to face detector portion
local_mqttclient.loop_start()




while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#print(type(gray), gray.shape)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		print('face detected', x,y,w,h)
		cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
		gray_face = gray[y:y+h, x:x+w]
		print(time.time())
		rc,png = cv2.imencode('.png', gray_face)
		msg = png.tobytes()
		if counter%cadence == 0:  # only save the 10th face
			with open('images/face'+str(counter)+'.png', 'wb') as file:
				file.write(msg)
			paho_publish("you got a face."+str(counter), local_mqttclient)
		counter += 1        
		#time.sleep(5)

	cv2.imshow('frame',gray)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		local_mqttclient.loop_stop()
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
