from django.shortcuts import render
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2 as cv
from keras_preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np

# Create your views here.

# parameters for loading data and images
detection_model_path = './static/haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = './static/models/_mini_XCEPTION.102-0.66.hdf5'

# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry" ,"disgust","scared", "happy", "sad", "surprised",
 "neutral"]


def VidFeed(request):
 return StreamingHttpResponse(Main(), content_type='multipart/x-mixed-replace;boundary=frame')


def Main():
 print("[INFO] starting video stream...")
 cap = cv.VideoCapture(0)
 while True:
  ret, frame = cap.read()
  if ret is False:
   break
  frame = imutils.resize(frame, width=600)

  # 시작
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

  frameClone = frame.copy()
  if len(faces) > 0:
   faces = sorted(faces, reverse=True,
                  key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
   (fX, fY, fW, fH) = faces

   roi = gray[fY:fY + fH, fX:fX + fW]
   roi = cv2.resize(roi, (64, 64))
   roi = roi.astype("float") / 255.0
   roi = img_to_array(roi)
   roi = np.expand_dims(roi, axis=0)

   preds = emotion_classifier.predict(roi)[0]
   emotion_probability = np.max(preds)
   label = EMOTIONS[preds.argmax()]
  else:
   continue

  for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
   text = "{}: {:.2f}%".format(emotion, prob * 100)

   cv2.putText(frameClone, label, (fX, fY - 10),
               cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
   cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),
                 (0, 0, 255), 2)

  imgencode = cv.imencode('.jpg', frameClone)[1]
  stringData = imgencode.tostring()
  yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')