import cv2
import numpy as np
import mediapipe as mp

source_video = "./jack.mp4"
#source_video = 0

cap = cv2.VideoCapture(source_video)

mpDraw = mp.solutions.drawing_utils

mpFaceMesh = mp.solutions.face_mesh

faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec1 = mpDraw.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=2)
drawSpec2 = mpDraw.DrawingSpec(color=(0,0,255), thickness=1, circle_radius=2)

# Get info about the input video

fps = cap.get(cv2.CAP_PROP_FPS) or 30  # fallback to 30 if it returns 0
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define output codec and create VideoWriter

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 'XVID' or 'MJPG' for AVI
out = cv2.VideoWriter('output_video2.mp4', fourcc, fps, (width, height))

while cap.isOpened():
    
    ret, img = cap.read()
    
    if not ret:
        break
    
    #scale_val = 0.8
    #x1 = int(img.shape[1] * scale_val)
    #x2 = int(img.shape[0] * scale_val)
    #img = cv2.resize(img, (x1, x2))

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    detections = faceMesh.process(imgRGB)

    if detections.multi_face_landmarks:
        for face_landmark in detections.multi_face_landmarks:
            mpDraw.draw_landmarks(img, face_landmark, mpFaceMesh.FACEMESH_CONTOURS, drawSpec1, drawSpec2)

    cv2.imshow("Face Mesh", img)
    out.write(img)    
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
