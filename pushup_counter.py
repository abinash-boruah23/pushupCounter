from itertools import count
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cam = cv2.VideoCapture(0)
counter = 0

position = None


with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
  while cam.isOpened():
    ret, frame = cam.read()

    # Recoloring
    rendered_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rendered_frame.flags.writeable = False
    
    results = pose.process(rendered_frame)
    
    rendered_frame.flags.writeable = True
    rendered_frame = cv2.cvtColor(rendered_frame, cv2.COLOR_RGB2BGR)

    #extracting landmarks
    try:
      landmarks = results.pose_landmarks.landmark
      
      right_diff1 = landmarks[14].y - landmarks[12].y
      right_diff2 = landmarks[24].y - landmarks[12].y

      left_diff1 = landmarks[13].y - landmarks[11].y
      left_diff2 = landmarks[23].y - landmarks[11].y

      if(len(landmarks)!=0):
        if(right_diff1 + left_diff1 < 0.2 and right_diff2 + left_diff2 < 0.2):
          position = "down"

        if(right_diff1 + left_diff1 > 0.2 and position=="down"):
          position = "up"
          counter+=1

    except:
      pass


    #text
    cv2.rectangle(rendered_frame, (0,0), (225,73), (147,61,247), -1)
    cv2.putText(rendered_frame, "Counter: " + str(counter), (25,45), 
                cv2.FONT_HERSHEY_COMPLEX, 1, (59,0,22), 1, cv2.LINE_AA)
    
    cv2.rectangle(rendered_frame, (0,rendered_frame.shape[0]), (rendered_frame.shape[1],rendered_frame.shape[0]-73), (147,61,247), -1)
    cv2.putText(rendered_frame, 'Press R to reset counters', (25,rendered_frame.shape[0]-25), 
                cv2.FONT_HERSHEY_COMPLEX, 1, (59,0,22), 1, cv2.LINE_AA)
    cv2.putText(rendered_frame, 'Press Q to Quit', (rendered_frame.shape[1] - 300,rendered_frame.shape[0]-25), 
                cv2.FONT_HERSHEY_COMPLEX, 1, (59,0,22), 1, cv2.LINE_AA)


    #rendering
    mp_drawing.draw_landmarks(rendered_frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(123,89,255), thickness=4, circle_radius=4), 
                                mp_drawing.DrawingSpec(color=(222,222,255), thickness=2, circle_radius=2) 
                                )               
        
    cv2.imshow("Pushup Counter", rendered_frame)

    if cv2.waitKey(1) & 0xFF == ord('r'):
        counter = 0
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
         break

cam.release()
cv2.destroyAllWindows