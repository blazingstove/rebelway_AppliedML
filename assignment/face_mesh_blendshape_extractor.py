import cv2
import numpy as np
import mediapipe as mp
import json

source_video = "jack.mp4"

cap = cv2.VideoCapture(source_video)

# Create a base options object with a Face Landmarker model

base_options = mp.tasks.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
options = mp.tasks.vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=True,
    num_faces=1
)

blendshape_data = []
debug=False

with mp.tasks.vision.FaceLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened(): 
    
        # Load the image using OpenCV and convert to RGB

        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create MediaPipe Image

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
       
        # Run the face detection

        result = landmarker.detect(mp_image)

        # Draw landmarks on the frame
        
        if debug:
            if result.face_landmarks:
                for landmark in result.face_landmarks[0]:
                    h, w, _ = frame.shape
                    x_px, y_px = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (x_px, y_px), 1, (0, 255, 0), -1)
            cv2.imshow('Face Landmarks', frame)

        # Record blendshape coefficients

        frame_shapes = {}
        for blendshape in result.face_blendshapes[0]:
            frame_shapes[blendshape.category_name] = blendshape.score
        blendshape_data.append(frame_shapes)
        
        if cv2.waitKey(1) == ord('q'):
           break

# Clean up

cap.release()
cv2.destroyAllWindows()

outputfile = 'face_blendshapes.json'

with open(outputfile, 'w') as f:
    json.dump(blendshape_data, f, indent=4)

print("Blendshape Data Saved!")
