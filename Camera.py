import threading
import socket
import json
import math
import time
import pandas as pd
import numpy as np
from statistics import mean, stdev
import datetime

# internal imports
from MP import MP
from Joint import Joint
import Settings as s
import Excel
from Audio import say
from performance_classification import feature_extraction, predict_performance, plot_data


class Camera(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # Create socket for client-server communication with Camera.py
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 7000)
        self.sock.bind(self.server_address)
        print("CAMERA INITIALIZATION")

    def get_skeleton_data(self):
        self.sock.settimeout(1)
        try:
            data, address = self.sock.recvfrom(4096)
            # print('received {} bytes from {}'.format(len(data), address))
            data = json.loads(data.decode())
            data = data.split('/')
            joints_str = []
            for i in data:
                joint_data = i.split(',')
                joints_str.append(joint_data)
            joints_str = joints_str[:-1]  # remove the empty list at the end
            # change from string to float values
            joints = {}  # joints dict data
            for j in joints_str:
                joints[j[0]] = Joint(j[0], float(j[1]), float(j[2]), float(j[3]) * 100)  # z is smaller than x and y!!
            return joints
        except socket.timeout:  # fail after 1 second of no activity
            print("Didn't receive data! [Timeout]")
            return None

    def init_position(self):
        # Check user position - so all joints all visible, and all exercise will be able to be recognized.
        init_pos = False
        say("calibration")
        print("CAMERA: init position - please stand in front of the camera with hands to the sides")
        while not init_pos:
            jd = self.get_skeleton_data()
            if jd is not None:
                count = 0
                for j in jd.values():
                    print(j)
                    if j.visible:
                        count += 1
                angle_right = self.calc_angle(jd["R_Shoulder"], jd["R_Hip"], jd["R_Wrist"])
                angle_left = self.calc_angle(jd["L_Shoulder"], jd["L_Hip"], jd["L_Wrist"])
                if count == len(jd) and angle_right > 80 and angle_left > 80:
                    init_pos = True  # all joints are visible + arms are raised to the sides - position initialized.
            else:  # skeleton is not recognized in frame
                print("user is not recognized")
        # say("calibration_complete")
        s.calibration = True
        print("CAMERA: init position verified")

    def calc_angle(self, joint1, joint2, joint3):
        a = self.calc_dist(joint1, joint2)
        b = self.calc_dist(joint1, joint3)
        c = self.calc_dist(joint2, joint3)
        try:
            rad_angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
            deg_angle = (rad_angle * 180) / math.pi
            return round(deg_angle, 2)
        except:
            # pass
            print("could not calculate the angle")

    def calc_angle_3d(self, joint1, joint2, joint3):
        if joint1.is_joint_all_zeros() or joint2.is_joint_all_zeros() or joint3.is_joint_all_zeros():
            return None

        a = np.array([joint1.x, joint1.y, joint1.z])  # First
        b = np.array([joint2.x, joint2.y, joint2.z])  # Mid
        c = np.array([joint3.x, joint3.y, joint3.z])  # End

        ba = a - b
        bc = c - b
        try:
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(cosine_angle)
            return round(np.degrees(angle), 2)

        except:
            print("could not calculate the angle")
            return None

    def calc_dist(self, joint1, joint2):
        distance = math.hypot(joint1.x - joint2.x,
                              joint1.y - joint2.y)
        return distance

    def exercise_two_angles_3d(self, exercise_name, joint1, joint2, joint3, up_lb, up_ub, down_lb, down_ub,
                               joint4, joint5, joint6, up_lb2, up_ub2, down_lb2, down_ub2, angle_classification, use_alternate_angles=False):
        flag = True
        counter = 0
        said_instructions = False
        list_joints = []
        while s.req_exercise == exercise_name:
            joints = self.get_skeleton_data()
            if joints is not None:
                right_angle = self.calc_angle_3d(joints[str("R_" + joint1)], joints[str("R_" + joint2)],
                                                 joints[str("R_" + joint3)])
                left_angle = self.calc_angle_3d(joints[str("L_" + joint1)], joints[str("L_" + joint2)],
                                                joints[str("L_" + joint3)])
                if use_alternate_angles:
                    right_angle2 = self.calc_angle_3d(joints[str("L_" + joint4)], joints[str("R_" + joint5)],
                                                      joints[str("R_" + joint6)])
                    left_angle2 = self.calc_angle_3d(joints[str("R_" + joint4)], joints[str("L_" + joint5)],
                                                     joints[str("L_" + joint6)])
                else:
                    right_angle2 = self.calc_angle_3d(joints[str("R_" + joint4)], joints[str("R_" + joint5)],
                                                   joints[str("R_" + joint6)])
                    left_angle2 = self.calc_angle_3d(joints[str("L_" + joint4)], joints[str("L_" + joint5)],
                                                  joints[str("L_" + joint6)])
                new_entry = [joints[str("R_" + joint1)], joints[str("R_" + joint2)], joints[str("R_" + joint3)],
                             joints[str("L_" + joint1)], joints[str("L_" + joint2)], joints[str("L_" + joint3)],
                             joints[str("R_" + joint4)], joints[str("R_" + joint5)], joints[str("R_" + joint6)],
                             joints[str("L_" + joint4)], joints[str("L_" + joint5)], joints[str("L_" + joint6)],
                             right_angle, left_angle, right_angle2, left_angle2]
                list_joints.append(new_entry)
                if s.one_hand != False:
                    if s.one_hand == 'right':
                        if not flag:
                            left_angle = up_ub-1
                            left_angle2 = up_ub2-1
                        else:
                            left_angle = down_ub-1
                            left_angle2 = down_ub2-1
                    else: # s.one_hand = left
                        if not flag:
                            right_angle = up_ub-1
                            right_angle2 = up_ub2-1
                        else:
                            right_angle = down_ub-1
                            right_angle2 = down_ub2-1
                if right_angle is not None and left_angle is not None and \
                        right_angle2 is not None and left_angle2 is not None:
                    if (up_lb < right_angle < up_ub) & (up_lb < left_angle < up_ub) & \
                            (up_lb2 < right_angle2 < up_ub2) & (up_lb2 < left_angle2 < up_ub2) & (not flag):
                        flag = True
                        counter += 1
                        print(counter)
                        if not s.robot_count:
                            say(str(counter))
                    if (down_lb < right_angle < down_ub) & (down_lb < left_angle < down_ub) & \
                            (down_lb2 < right_angle2 < down_ub2) & (down_lb2 < left_angle2 < down_ub2) & (flag):
                        flag = False
            if (not s.robot_count) and (counter == s.rep):
                s.req_exercise = ""
                s.success_exercise = True
                break
            if s.corrective_feedback and (s.robot_rep >= s.rep/2) and counter <=2 and not said_instructions:
                say(exercise_name + "_" + str(flag))
                said_instructions = True
                if flag:
                    print("Corrective feedback true - Try to raise your hands more")
                if not flag:
                    print("Corrective feedback false - Try to close your hands more")
        if s.adaptive:
            try:
                if angle_classification == "first":
                    self.classify_performance(list_joints, exercise_name, 12, 13, counter)
                else:
                    self.classify_performance(list_joints, exercise_name, 14, 15, counter)
            except Exception as e:
                print (f"can't do classification {e}")
        if s.one_hand=='right':
            exercise_name = exercise_name[:-9]
        elif s.one_hand=='left':
            exercise_name = exercise_name[:-9]
        s.ex_list.append([exercise_name, counter])
        Excel.wf_joints(exercise_name, list_joints)

    def exercise_one_angle_3d(self, exercise_name, joint1, joint2, joint3, up_lb, up_ub, down_lb, down_ub,
                              use_alternate_angles=False):
        flag = True
        counter = 0
        said_instructions = False
        list_joints = []
        while s.req_exercise == exercise_name:
            joints = self.get_skeleton_data()
            if joints is not None:
                if use_alternate_angles:
                    right_angle = self.calc_angle_3d(joints[str("L_" + joint1)], joints[str("R_" + joint2)],
                                                     joints[str("R_" + joint3)])
                    left_angle = self.calc_angle_3d(joints[str("R_" + joint1)], joints[str("L_" + joint2)],
                                                    joints[str("L_" + joint3)])
                else:
                    right_angle = self.calc_angle_3d(joints[str("R_" + joint1)], joints[str("R_" + joint2)],
                                                     joints[str("R_" + joint3)])
                    left_angle = self.calc_angle_3d(joints[str("L_" + joint1)], joints[str("L_" + joint2)],
                                                    joints[str("L_" + joint3)])

                new_entry = [joints[str("R_" + joint1)], joints[str("R_" + joint2)], joints[str("R_" + joint3)],
                             joints[str("L_" + joint1)], joints[str("L_" + joint2)], joints[str("L_" + joint3)],
                             right_angle, left_angle]
                list_joints.append(new_entry)
                if right_angle is not None and left_angle is not None:
                    if (up_lb < right_angle < up_ub) & (up_lb < left_angle < up_ub) & (not flag):
                        flag = True
                        counter += 1
                        print(counter)
                        if not s.robot_count:
                            say(str(counter))
                    if (down_lb < right_angle < down_ub) & (down_lb < left_angle < down_ub) & (flag):
                        flag = False
            if (not s.robot_count) and (counter == s.rep):
                s.req_exercise = ""
                s.success_exercise = True
                break
            if s.corrective_feedback and (s.robot_rep >= s.rep/2) and counter <=2 and not said_instructions:
                say(exercise_name + "_" + str(flag))
                said_instructions = True
                if flag:
                    print("Try to raise your hands more")
                if not flag:
                    print("Try to close your hands more")

        if s.adaptive:
            self.classify_performance(list_joints, exercise_name, 6, 7, counter)
        s.ex_list.append([exercise_name, counter])
        Excel.wf_joints(exercise_name, list_joints)

    def impossible_EX(self):
        self.exercise_two_angles_3d("impossible_EX","Shoulder", "Elbow", "Wrist", 85, 95, 80, 100,
                                    "Elbow","Shoulder", "Wrist", 85, 95, 0, 360, "first", True)
    def raise_arms_horizontally(self):
        self.exercise_two_angles_3d("raise_arms_horizontally", "Hip", "Shoulder", "Wrist", 80, 105, 5, 30,
                                    "Shoulder", "Shoulder", "Wrist", 150, 180, 80, 110, "first", True)

    def bend_elbows(self):
        self.exercise_one_angle_3d("bend_elbows", "Shoulder", "Elbow", "Wrist", 150, 180, 10, 50) #todo change to 2 angles - add armpit

    def raise_arms_bend_elbows(self):
        self.exercise_two_angles_3d("raise_arms_bend_elbows", "Shoulder", "Elbow", "Wrist", 130, 180, 10, 70,
                                    "Elbow", "Shoulder", "Hip", 60, 105, 60, 105, "first")

    def raise_arms_bend_elbows_one_hand(self):
        self.exercise_two_angles_3d("raise_arms_bend_elbows_one_hand", "Shoulder", "Elbow", "Wrist", 130, 180, 10, 70,
                                    "Elbow", "Shoulder", "Hip", 60, 105, 60, 105, "first")

    def open_and_close_arms(self):
        self.exercise_two_angles_3d("open_and_close_arms",  "Hip", "Shoulder", "Wrist", 80, 150, 80, 150,
                                   "Shoulder", "Shoulder", "Wrist", 90, 120, 150, 175, "second",  True)

    def open_and_close_arms_one_hand(self):
        self.exercise_two_angles_3d("open_and_close_arms_one_hand",  "Hip", "Shoulder", "Wrist", 80, 150, 80, 150,
                                   "Shoulder", "Shoulder", "Wrist", 90, 120, 150, 175, "second",  True)

    def open_and_close_arms_90(self):
        self.exercise_two_angles_3d("open_and_close_arms_90", "Wrist", "Elbow", "Shoulder", 60, 150, 60, 150,
                                    "Shoulder", "Shoulder", "Elbow", 140, 180, 80, 120, "second", True)

    def open_and_close_arms_90_one_hand(self):
        self.exercise_two_angles_3d("open_and_close_arms_90_one_hand", "Wrist", "Elbow", "Shoulder", 60, 150, 60, 150,
                                    "Shoulder", "Shoulder", "Elbow", 140, 180, 80, 120, "second", True)

    def raise_arms_forward(self):
        self.exercise_two_angles_3d("raise_arms_forward", "Wrist", "Shoulder", "Hip", 85, 135, 10, 50,
                                   "Shoulder", "Shoulder", "Wrist", 80, 115, 80, 115, "first", True)

    def raise_arms_forward_one_hand(self):
        self.exercise_two_angles_3d("raise_arms_forward_one_hand", "Wrist", "Shoulder", "Hip", 85, 135, 10, 50,
                                   "Shoulder", "Shoulder", "Wrist", 80, 115, 80, 115, "first", True)
    def check_hello_wave(self):
    
        print("Checking for hello_wave motion...")
        joints = self.get_skeleton_data()  # Fetch skeleton data
        if joints is not None:
         right_shoulder = joints.get("R_Shoulder")
         right_wrist = joints.get("R_Wrist")

        # Check if the wrist is above the shoulder, indicating a wave
        if right_shoulder and right_wrist and right_wrist.y > right_shoulder.y:
            print("Hello_wave detected! Exiting function.")
            return True  # Indicate that waving was detected
        return False  # Indicate that no waving was detected

    def hello_waving(self):  # check if the participant waved
        if s.try_again:
            print("Camera: Wave for trying again")
            say('try again')
        else:
            time.sleep(4)
            print("Camera: Wave for start")
            say('ready wave')
        while s.req_exercise == "hello_waving":
            joints = self.get_skeleton_data()
            if joints is not None:
                right_shoulder = joints[str("R_Shoulder")]
                right_wrist = joints[str("R_Wrist")]
                if right_shoulder.y < right_wrist.y != 0:
                    # print(right_shoulder.y)
                    # print(right_wrist.y)
                    s.waved = True
                    s.req_exercise = ""

    def check_angle_range(self, joint1, joint2, joint3, use_alternate_angles=False):
        # just for coding and understanding angle boundaries
        list_joints = []
        list_joints2 = []
        medaip = MP()
        medaip.start()
        s.finish_workout = False
        while not s.finish_workout:
            joints = self.get_skeleton_data()
            if joints is not None:
                if use_alternate_angles:
                    right_angle = self.calc_angle_3d(joints[str("L_" + joint1)], joints[str("R_" + joint2)],
                                                     joints[str("R_" + joint3)])
                    left_angle = self.calc_angle_3d(joints[str("R_" + joint1)], joints[str("L_" + joint2)],
                                                    joints[str("L_" + joint3)])
                else:
                    right_angle = self.calc_angle_3d(joints[str("R_" + joint1)], joints[str("R_" + joint2)],
                                                     joints[str("R_" + joint3)])
                    left_angle = self.calc_angle_3d(joints[str("L_" + joint1)], joints[str("L_" + joint2)],
                                                    joints[str("L_" + joint3)])
                if right_angle is not None:  # and right_angle2 is not None:
                    list_joints.append(right_angle)
                    # list_joints2.append(right_angle2)
                    # list_joints.append(left_angle)
        print(list_joints)
        print(mean(list_joints))
        print(stdev(list_joints))

        # print(list_joints2)
        # print(mean(list_joints2))
        # print(stdev(list_joints2))

    def classify_performance(self, list_joints, exercise_name, indexangleright, indexangleleft, counter):
        if counter > 1:
            df = pd.DataFrame([sublist[indexangleright:indexangleleft + 1] for sublist in
                               list_joints]).T  # angles are in the indexangleright and indexangleleft indexs
            right_hand_data = df.iloc[0]
            right_hand_data = right_hand_data.dropna().to_numpy()
            left_hand_data = df.iloc[1]
            left_hand_data = left_hand_data.dropna().to_numpy()

            features = feature_extraction(right_hand_data, left_hand_data)
            exercise = exercise_name
            predictions = predict_performance(features, exercise, s.adaptation_model_name)
            if exercise in s.performance_class:
                current_time = datetime.datetime.now()
                s.performance_class[exercise + str(current_time.minute) + str(current_time.second)] = {'right': predictions[1], 'left': predictions[0]}
            else:
                s.performance_class[exercise] = {'right': predictions[1], 'left': predictions[0]}
            print(f"CAMERA: performance classification {s.performance_class}")
            plot_data(exercise_name, right_hand_data, left_hand_data)  # only for internal checks comparing plot to classification
        else:
            s.performance_class[exercise_name] = {'right': 1, 'left': 1}  # the exercise was not performed enough times

    def run(self):
        print("CAMERA START")
        medaip = MP()
        medaip.start()

        while not s.finish_workout:
            time.sleep(0.00000001)  # Prevents the MP to stuck
            jd = self.get_skeleton_data()  # clear data TODO check if it help
            if s.req_exercise != "":
                print("CAMERA: Exercise ", s.req_exercise, " start")
                time.sleep(1)
                getattr(self, s.req_exercise)()
                print("CAMERA: Exercise ", s.req_exercise, " done")
                s.req_exercise = ""
                s.camera_done = True
        print("Camera Done")


if __name__ == '__main__':
    check = False
    if check:
        c = Camera()
        # c.check_angle_range("Shoulder", "Hip", "Wrist")
        c.check_angle_range( "Shoulder", "Shoulder", "Wrist", True)

    else:
        language = 'Hebrew'
        gender = 'Female'
        s.audio_path = 'audio files/' + language + '/' + gender + '/'
        s.finish_workout = False
        s.participant_code = "1106"
        s.rep = 2
        s.corrective_feedback = False
        s.one_hand = 'right'
        s.req_exercise = "raise_arms_bend_elbows_one_hand"
        s.robot_count = False
        Excel.create_workbook()
        s.ex_list = []
        s.adaptive = True
        if s.adaptive:
            s.adaptation_model_name = 'model2'
            s.performance_class = {}
        print('HelloServer')
        c = Camera()
        c.start()
