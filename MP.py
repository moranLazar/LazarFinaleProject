
import threading
import socket
import json
import threading
import cv2
import mediapipe as mp
import Settings as s
import time


class MP(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print("MP INITIALIZATION")

    def run(self):
        print("MP START")
        recorded_data = []
        show = True
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose

        cap = cv2.VideoCapture(0) # 0 - webcam, 2 - second USB in maya's computer
        image_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1680)
        image_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
        with mp_pose.Pose(
                min_detection_confidence=0.8,
                min_tracking_confidence=0.5) as pose:

            #Create a UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = ('localhost', 7000)

            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = pose.process(image)

                lm_dict = {'nose': "0",
                         'L_eye_inner': "1", 'L_eye': "2", "L_eye_outer": "3",
                         'R_eye_inner': "4", 'R_eye': "5", "R_eye_outer": "6",
                         'L_ear': "7", 'R_ear': "8", "L_mouth": "9","R_mouth": "10",
                         'L_Shoulder': "11", 'R_Shoulder': "12", 'L_Elbow': "13", 'R_Elbow': "14",
                         'L_Wrist': "15", 'R_Wrist': "16",
                         'L_pinky': "17", 'R_pinky': "18", 'L_index': "19", 'R_index': "20",
                         'L_thumb': "21", 'R_thumb': "22", 'L_Hip': "23", 'R_Hip': "24"}

                # 'L_knee': "25", 'R_knee': "26", 'L_ankle': "27", 'R_ankle': "28",
                # 'L_heel': "29", 'R_heel': "30", 'L_foot_index': "31", 'R_foot_index': "32"}

                message = ''
                if results.pose_landmarks is not None:
                    for k, v in lm_dict.items():
                        j = results.pose_landmarks.landmark[int(v)]
                        if j.visibility >= 0.7:
                            new_j = k + "," + str(j.x*image_width) + "," + str(-j.y*image_height) + "," + str(-j.z)
                        else:
                            new_j = k + ",0,0,0"
                        message += new_j + "/"
                else:
                    for k, v in lm_dict.items():
                        new_j = k + ",0,0,0"
                        message += new_j + "/"

                jsonmessage = json.dumps(message).encode()
                # print("Sending a message...")
                sent = sock.sendto(jsonmessage, server_address)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                ## plot pose graph
                # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                # Present camera's video: Flip the image horizontally for a selfie-view display.
                if show:
                    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

                # Stop MediaPipe:
                key = cv2.waitKey(1) #TODO change
                if s.finish_workout or key == ord('q'):
                    s.finish_workout = True
                    break

                recorded_data.append({
                    'timestamp': time.time(),
                    'json_message': message
                })

            cap.release()

            # Save recorded data to a JSON file
            with open('recorded_data2.json', 'w') as f:
                json.dump(recorded_data, f)


if __name__ == '__main__':
    s.stop = False
    mediap = MP()
    mediap.start()
    s.finish_workout = False



