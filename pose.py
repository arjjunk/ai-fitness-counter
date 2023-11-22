import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import filedialog
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def capture_live_photo():

    cap = cv2.VideoCapture(0)

# Curl counter variables
    counter = 0 
    stage = None

## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
        
        # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
      
        # Make detection
            results = pose.process(image)
    
        # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
            def calculate_angle(a,b,c):
                a = np.array(a) # First
                b = np.array(b) # Mid
                c = np.array(c) # End
    
                radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
                angle = np.abs(radians*180.0/np.pi)
    
                if angle >180.0:
                    angle = 360-angle
        
                return angle 
        # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # Calculate angle
                angle = calculate_angle(shoulder, elbow, wrist)
            
            # Visualize angle
                cv2.putText(image, str(angle), 
                               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
            
            # Curl counter logic
                if angle > 160:
                    stage = "down"
                if angle < 30 and stage =='down':
                    stage="up"
                    counter +=1
                    print(counter)
                       
            except:
                pass
        
        # Render curl counter
        # Setup status box
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )               
        
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()




def counter():

    cap = cv2.VideoCapture(0)

# Curl counter variables
    counter = 0 
    stage = None

## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
        
        # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
      
        # Make detection
            results = pose.process(image)
    
        # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
            def calculate_angle(a,b,c):
                a = np.array(a) # First
                b = np.array(b) # Mid
                c = np.array(c) # End
    
                radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
                angle = np.abs(radians*180.0/np.pi)
    
                if angle >180.0:
                    angle = 360-angle
        
                return angle 
        # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            
            # Calculate angle
                angle = calculate_angle(shoulder, elbow, hip)
            
            # Visualize angle
                cv2.putText(image, str(angle), 
                               tuple(np.multiply(shoulder, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
            
            # Curl counter logic
                if angle < 60 and angle > 0:
                    stage = "up"
                if angle > 120 and angle <180 and stage == "up":
                    stage="down"
                    counter +=1
                    print(counter)
                       
            except:
                pass
        
        # Render curl counter
        # Setup status box
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )               
        
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()




def hipexercise():

    cap = cv2.VideoCapture(0)

# Curl counter variables
    counter = 0 
    stage = None

## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
        
        # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
      
        # Make detection
            results = pose.process(image)
    
        # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
            def calculate_angle(a,b,c):
                a = np.array(a) # First
                b = np.array(b) # Mid
                c = np.array(c) # End
    
                radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
                angle = np.abs(radians*180.0/np.pi)
    
                if angle >180.0:
                    angle = 360-angle
        
                return angle 
        # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            
            # Calculate angle
                angle = calculate_angle(shoulder, hip, knee)
            
            # Visualize angle
                cv2.putText(image, str(angle), 
                               tuple(np.multiply(hip, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
            
            # Curl counter logic
                if angle > 130 and angle < 200:
                    stage = "up"
                if angle < 120 and angle > 0 and stage == "up":
                    stage="down"
                    counter +=1
                    print(counter)
                       
            except:
                pass
        
        # Render curl counter
        # Setup status box
            cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )               
        
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        
my_w = tk.Tk()
my_w.geometry("800x500")  # Adjusted the window size
my_w.title('AI Fitness')
my_font1 = ('times', 18, 'bold')



l2 = tk.Label(my_w, text='Curl count :', width=30, font=my_font1)
l2.grid(row=1, column=1)

b2 = tk.Button(my_w, text='Open Camera', width=20, command=capture_live_photo)
b2.grid(row=1, column=2)

l2 = tk.Label(my_w, text='Count :', width=30, font=my_font1)
l2.grid(row=2, column=1)

b2 = tk.Button(my_w, text='Open Camera', width=20, command=counter)
b2.grid(row=2, column=2)

l2 = tk.Label(my_w, text='Hip exercise :', width=30, font=my_font1)
l2.grid(row=3, column=1)

b2 = tk.Button(my_w, text='Open Camera', width=20, command=hipexercise)
b2.grid(row=3, column=2)

#img_label = tk.Label(my_w)
#img_label.grid(row=3, column=1)

my_w.mainloop()
