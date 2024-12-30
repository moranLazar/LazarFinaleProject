import threading
from pypot.creatures import PoppyTorso
import time
import Settings as s
from Audio import say
import Screen as screen


class Poppy(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.poppy = PoppyTorso(camera="dummy")  # for real robot
        #self.poppy = PoppyTorso(simulator='vrep')  # for simulator
        print("ROBOT INITIALIZATION")
        for m in self.poppy.motors:  # motors need to be initialized, False=stiff, True=loose
            m.compliant = False
        self.init_robot()

    def init_robot(self):
        for m in self.poppy.motors:
            if not m.name == 'r_elbow_y' and not m.name == 'l_elbow_y' and not m.name == 'head_y':
                m.goto_position(0, 1, wait=True)
        self.poppy.head_y.goto_position(-20, 1, wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=True)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=True)

    def run(self):
        print("POPPY START")
        while True:
            if s.req_exercise != "":
                print(f"Poppy received exercise request: {s.req_exercise}")  # Debug print
                if s.req_exercise == "open_and_close_arms_90":
                    print("Executing open_and_close_arms_90...")  # Debug print
                    self.open_and_close_arms_90()
                # ... other exercise conditions ...
                s.req_exercise = ""
            time.sleep(0.001)

    def exercise_demo(self, ex):
        if ex == "hello_waving":
            self.hello_waving()
        if ex=="check_hello_wave":
            self.check_hello_wave()
        else:
            for i in range(s.rep):
                s.robot_rep = i
                getattr(self, ex)(i)
                if s.success_exercise:
                    break
    
    def check_hello_wave(self):
        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-80, 1.5, wait=False)
        for i in range(3):
             self.poppy.r_arm[3].goto_position(-35, 0.6, wait=True)
             self.poppy.r_arm[3].goto_position(35, 0.6, wait=True)
        self.finish_waving()

    def hello_waving(self):
        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(-20, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-80, 1.5, wait=False)
        for i in range(3):
            self.poppy.r_arm[3].goto_position(-35, 0.6, wait=True)
            self.poppy.r_arm[3].goto_position(35, 0.6, wait=True)
        self.finish_waving()

    def finish_waving(self):
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)

    #impossible EX  
    def impossible_EX(self):
    # Step 1: Raise arms to a 90-degree angle from the armpit
        print("Step 1: Lifting arms to 90 degrees")
        self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False)  # Left shoulder to 90 degrees
        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False)  # Right shoulder to -90 degrees
        time.sleep(1.5)

    # Step 2: Bend elbows to a 90-degree angle
        print("Step 2: Bending elbows to 90 degrees")
        self.poppy.l_elbow_y.goto_position(-90, 1.5, wait=False)  # Left elbow to -90 degrees
        self.poppy.r_elbow_y.goto_position(-90, 1.5, wait=False)  # Right elbow to -90 degrees
        time.sleep(1.5)

    # Step 3: Rotate elbows to simulate a 360-degree motion
        print("Step 3: Rotating elbows 360 degrees")
        for _ in range(2):  # Two full rotations
            self.poppy.l_elbow_y.goto_position(90, 1.0, wait=False)  # Rotate left elbow forward
            self.poppy.r_elbow_y.goto_position(90, 1.0, wait=False)  # Rotate right elbow forward
            time.sleep(1.0)
            self.poppy.l_elbow_y.goto_position(-90, 1.0, wait=False)  # Rotate left elbow back
            self.poppy.r_elbow_y.goto_position(-90, 1.0, wait=False)  # Rotate right elbow back
            time.sleep(1.0)

    # Return to the initial position
        print("Returning to initial position")
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)  # Left shoulder to neutral
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)  # Right shoulder to neutral
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)  # Left elbow to 90 degrees
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)  # Right elbow to 90 degrees
        time.sleep(3)


    #impossible EX ADAPTIVE 
    def impossible_EX_Adaptive(self):
    # Step 1: Raise arms to a 90-degree angle from the armpit
        print("Step 1: Lifting arms to 90 degrees")
        self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False)  # Left shoulder to 90 degrees
        self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False)  # Right shoulder to -90 degrees
        time.sleep(1.5)

    # Step 2: Bend elbows to a 90-degree angle
        print("Step 2: Bending elbows to 90 degrees")
        self.poppy.l_elbow_y.goto_position(-90, 1.5, wait=False)  # Left elbow to -90 degrees
        self.poppy.r_elbow_y.goto_position(-90, 1.5, wait=False)  # Right elbow to -90 degrees
        time.sleep(1.5)

    # Step 3: Rotate elbows to simulate a 360-degree motion
        print("Step 3: Rotating elbows 360 degrees")
        for _ in range(2):  # Two full rotations
            self.poppy.l_elbow_y.goto_position(90, 1.0, wait=False)  # Rotate left elbow forward
            self.poppy.r_elbow_y.goto_position(90, 1.0, wait=False)  # Rotate right elbow forward
            time.sleep(1.0)
            self.poppy.l_elbow_y.goto_position(-90, 1.0, wait=False)  # Rotate left elbow back
            self.poppy.r_elbow_y.goto_position(-90, 1.0, wait=False)  # Rotate right elbow back
            time.sleep(1.0)

    # Return to the initial position
        print("Returning to initial position")
        self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)  # Left shoulder to neutral
        self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)  # Right shoulder to neutral
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)  # Left elbow to 90 degrees
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)  # Right elbow to 90 degrees
        time.sleep(1.5)
        
    # EX1 - Raise arms horizontally
    def raise_arms_horizontally(self, counter):
        hands_up = [self.poppy.l_shoulder_x.goto_position(90, 1.5, wait=False),
                    self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                    self.poppy.r_shoulder_x.goto_position(-90, 1.5, wait=False),
                    self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
        time.sleep(2)
        hands_down = [self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False),
                      self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False),
                      self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False),
                      self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)]
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1.8)

    # EX2 - Bend Elbows
    def bend_elbows(self, counter):
        self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)
        time.sleep(1.5)
        self.poppy.r_arm[3].goto_position(85, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1.4)

    # EX3 - Raise Arms Bend Elbows
    def raise_arms_bend_elbows(self, counter):
        l_hand = [self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False),
                  self.poppy.l_arm_z.goto_position(-90, 2, wait=False),
                  self.poppy.l_shoulder_x.goto_position(50, 2, wait=False),
                  self.poppy.l_elbow_y.goto_position(-50, 2, wait=False)]
        r_hand = [self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False),
                  self.poppy.r_arm_z.goto_position(90, 2, wait=False),
                  self.poppy.r_shoulder_x.goto_position(-50, 2, wait=False),
                  self.poppy.r_elbow_y.goto_position(-50, 2, wait=True)]
        time.sleep(1.2)
        self.poppy.r_shoulder_x.goto_position(-85, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(95, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1)
        if counter >= s.rep-1 or s.success_exercise:  # TODO - Change to something that works if it finished before 8 repetitions.
            # return to init position
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    # EX3 - Raise Arms Bend Elbows One Hand
    def raise_arms_bend_elbows_one_hand(self, counter):
        if s.one_hand == 'right': # mirror demo
            l_hand = [self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False),
                      self.poppy.l_arm_z.goto_position(-90, 2, wait=False),
                      self.poppy.l_shoulder_x.goto_position(50, 2, wait=False),
                      self.poppy.l_elbow_y.goto_position(-50, 2, wait=True)]
            time.sleep(1.2)
            self.poppy.l_shoulder_x.goto_position(95, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        else:
            r_hand = [self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False),
                      self.poppy.r_arm_z.goto_position(90, 2, wait=False),
                      self.poppy.r_shoulder_x.goto_position(-50, 2, wait=False),
                      self.poppy.r_elbow_y.goto_position(-50, 2, wait=True)]
            time.sleep(1.2)
            self.poppy.r_shoulder_x.goto_position(-85, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1)
        if counter >= s.rep-1 or s.success_exercise:  # TODO - Change to something that works if it finished before 8 repetitions.
            # return to init position
            if s.one_hand == 'right': # mirror demo
                self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
                self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
                self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            else:
                self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
                self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
                self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    # Ex4 - open and close arms
    def open_and_close_arms(self, counter):
        if counter == 0:
            self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False)
        self.poppy.r_shoulder_x.goto_position(-85, 1.5, wait=False)
        self.poppy.l_shoulder_x.goto_position(95, 1.5, wait=False)
        # self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
        # self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
        time.sleep(1.8)
        self.poppy.l_shoulder_x.goto_position(0, 2, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 2, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1)
        if counter >= s.rep-1 or s.success_exercise:  # TODO - Change to something that works if it finished before 8 repetitions.
            self.poppy.l_shoulder_y.goto_position(0, 2, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 2, wait=False)
            self.poppy.l_shoulder_x.goto_position(0, 2, wait=False)
            self.poppy.r_shoulder_x.goto_position(0, 2, wait=True)

    # Ex4 - open and close arms - one hand
    def open_and_close_arms_one_hand(self, counter):
        if counter == 0:
            if s.one_hand == 'right':  # mirror demo
                self.poppy.l_shoulder_y.goto_position(-90, 2, wait=False)
            else:
                self.poppy.r_shoulder_y.goto_position(-90, 2, wait=False)
        if s.one_hand == 'right':
            self.poppy.l_shoulder_x.goto_position(95, 1.5, wait=False)
            time.sleep(1.8)
            self.poppy.l_shoulder_x.goto_position(0, 2, wait=False)
        else:
            self.poppy.r_shoulder_x.goto_position(-85, 1.5, wait=False)
            time.sleep(1.8)
            self.poppy.r_shoulder_x.goto_position(0, 2, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1)
        if counter >= s.rep-1 or s.success_exercise:  # TODO - Change to something that works if it finished before 8 repetitions.
            if s.one_hand == 'right':
                self.poppy.l_shoulder_y.goto_position(0, 2, wait=False)
                self.poppy.l_shoulder_x.goto_position(0, 2, wait=False)

            else:
                self.poppy.r_shoulder_y.goto_position(0, 2, wait=False)
                self.poppy.r_shoulder_x.goto_position(0, 2, wait=True)

    # EX5 - open and close arms 90
    def open_and_close_arms_90(self, counter):
        if counter == 0:
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
            self.poppy.l_elbow_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_elbow_y.goto_position(0, 1.5, wait=True)
        self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
        self.poppy.r_shoulder_x.goto_position(-90, 1, wait=True)
        time.sleep(1.8)
        self.poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        self.poppy.r_shoulder_x.goto_position(0, 1, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1)
        if counter >= s.rep-1 or s.success_exercise:  # need to change it to constant
            self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    # EX 6 raise_arms_forward
    def raise_arms_forward(self, counter):
        self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
        self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
        time.sleep(1.8)
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1)
        return

    # EX 6 raise_arms_forward - one hand
    def raise_arms_forward_one_hand(self, counter):
        if s.one_hand == 'right':  # mirror demo
            self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.l_arm_z.goto_position(-90, 1.5, wait=False)
            time.sleep(1.8)
            self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
        else:
            self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=False)
            self.poppy.r_arm_z.goto_position(90, 1.5, wait=False)
            time.sleep(1.8)
            self.poppy.r_arm_z.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1)


if __name__ == "__main__":
    s.rep = 3
    s.robot_count = True
    s.success_exercise = False
    s.finish_workout = False
    s.one_hand = 'left'
    language = 'Hebrew'
    gender = 'Male'
    s.audio_path = 'audio files/' + language + '/' + gender + '/'

    robot = Poppy()

    # robot.exercise_demo("open_and_close_arms_90")
    robot.exercise_demo("raise_arms_horizontally")
    # robot.start()
    time.sleep(10)

    # robot.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
    # robot.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
    # robot.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
    # # robot.poppy.r_shoulder_x.goto_position(-90, 1, wait=True)
    # robot.poppy.l_elbow_y.goto_position(0, 1.5, wait=False)
    # robot.poppy.r_elbow_y.goto_position(0, 1.5, wait=True)

