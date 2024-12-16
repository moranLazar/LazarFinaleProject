'''
Code Template from: https://google.github.io/mediapipe/solutions/pose.html
'''
import threading
import cv2
import mediapipe as mp
import numpy as np
from Joint import joint
import math


class Detection (threading.Thread):

    def angle_calc(self, joint1, joint2, joint3):
        a = np.array([joint1.x, joint1.y, joint1.z])
        b = np.array([joint2.x, joint2.y, joint2.z])
        c = np.array([joint3.x, joint3.y, joint3.z])
        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        return angle

    def calc_angle(self, joint1, joint2, joint3):
        a = self.calc_dist(joint1, joint2)
        b = self.calc_dist(joint1, joint3)
        c = self.calc_dist(joint2, joint3)
        try:
            rad_angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
            deg_angle = (rad_angle * 180) / math.pi
            return round(deg_angle, 2)
        except:
            print("could not calculate the angle")

    # Calculate distance between joints
    def calc_dist(self, joint1, joint2):
        distance = math.hypot(joint1.x - joint2.x,
                              joint1.y - joint2.y)
        return distance

    def start(self, ex_list, show=False):
        # Settings of mediapipe soultions for pose detection
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_pose = mp.solutions.pose

        cap = cv2.VideoCapture(2) # 0 - webcam, 2 - second USB in maya's computer
        image_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
        image_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
        with mp_pose.Pose(
                min_detection_confidence=0.8,
                min_tracking_confidence=0.5) as pose:
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

                # Get landmarks (joints) coordinates
                lm_dict={'nose': "0",
                         'L_eye_inner': "1", 'L_eye': "2", "L_eye_outer": "3",
                         'R_eye_inner': "4", 'R_eye': "5", "R_eye_outer": "6",
                         'L_ear': "7", 'R_ear': "8", "L_mouth": "9","R_mouth": "10",
                         'L_Shoulder': "11", 'R_Shoulder': "12", 'L_Elbow': "13", 'R_Elbow': "14",
                         'L_Wrist': "15", 'R_Wrist': "16",
                         'L_pinky': "17", 'R_pinky': "18", 'L_index': "19", 'R_index': "20",
                         'L_thumb': "21", 'R_thumb': "22", 'L_hip': "23", 'R_hip': "24"}

                # 'L_knee': "25", 'R_knee': "26", 'L_ankle': "27", 'R_ankle': "28",
                # 'L_heel': "29", 'R_heel': "30", 'L_foot_index': "31", 'R_foot_index': "32"}

                new_entry = []
                if results.pose_landmarks is not None:
                    for k, v in lm_dict.items():
                        j = results.pose_landmarks.landmark[int(v)]
                        if j.visibility >= 0.7:
                            print("joint name: %s, coordinates: '%s" %(k, j))
                            new_j = joint(k, j.x*image_width, -j.y*image_height, -j.z)
                        else:
                            new_j = joint(k, 0, 0, 0)
                        new_entry.append(new_j)

                    angle = self.angle_calc(new_entry[24],new_entry[12],new_entry[16])
                    angle2 = self.calc_angle(new_entry[24],new_entry[12],new_entry[16])
                    new_entry.append(angle)
                    new_entry.append(angle2)
                    ex_list.append(new_entry)

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

                mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                # Present camera's video: Flip the image horizontally for a selfie-view display.
                if show:
                    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

        cap.release()
        return ex_list


if __name__ == '__main__':
    import xlsxwriter
    import datetime

    raise_arms_horz = {'right':['R_hip', 'R_Shoulder', 'R_Wrist'], 'left':['L_hip', 'L_Shoulder', 'L_Wrist']}

    ex_list = [list(range(1, 32))]
    d = Detection()
    ex_list = d.start(ex_list, True)

    current_time = datetime.datetime.now()
    name = str(current_time.day) + "." + str(current_time.month) + " " + str(current_time.hour) + "." + \
           str(current_time.minute) + "." + str(current_time.second) + ".xlsx"
    excel_workbook = xlsxwriter.Workbook(name)
    worksheet = excel_workbook.add_worksheet()
    frame_number = 1
    for l in range(1, len(ex_list)):
        row = 1
        worksheet.write(0, frame_number, frame_number)
        for j in ex_list[l]:
            if type(j) == joint:
                j_ar = j.joint_to_array()
                for i in range(len(j_ar)):
                    worksheet.write(row, frame_number, str(j_ar[i]))
                    row += 1
            else:
                worksheet.write(row, frame_number, str(j))
                row += 1
        frame_number += 1

    excel_workbook.close()