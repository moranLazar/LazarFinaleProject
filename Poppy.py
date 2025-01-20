import threading
from pypot.creatures import PoppyTorso
import time
import Settings as s
from Audio import say
from Screen import one,two,three,four,five,six,seven,eight
import Settings as s

class Poppy(threading.Thread):
    def what_to_say(self,number):
     counter_to_write = {
    "1": one,
    "2": two,
    "3": three,
    "4": four,
    "5": five,
    "6": six,
    "7": seven,
    "8": eight,
}
     return counter_to_write.get(number, None)

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
        self.poppy.head_y.goto_position(0, 1, wait=True)
        self.poppy.r_elbow_y.goto_position(90, 1, wait=True)
        self.poppy.l_elbow_y.goto_position(90, 1, wait=True)

    def run(self):
        print("ROBOT START")
        while not s.finish_workout:
            time.sleep(0.00000001)  # Prevents the MP to stuck
            if s.req_exercise != "" and not ((s.req_exercise=="hello_waving" and s.try_again) or (s.req_exercise=="hello_waving" and s.try_again)or (s.req_exercise=="impossible_EX" and s.try_again)): # if there is exercise, or hello waving
                time.sleep(1)
                print("ROBOT: Exercise ", s.req_exercise, " start")
                self.exercise_demo(s.req_exercise)
                print("ROBOT: Exercise ", s.req_exercise, " done")
                if not s.calibration: #meaning it's the first hello
                    while not s.waved:
                        time.sleep(0.01)  # for hello_waiting exercise, wait until user wave
                s.req_exercise = ""
                s.poppy_done = True
        print("Robot Done")

    def exercise_demo(self, ex):
     if ex == "hello_waving":
        self.hello_waving()
     elif ex == "check_hello_wave":
        self.check_hello_wave()
     elif ex == "impossible_EX":
        self.impossible_EX()
        if s.success_exercise :
            if (s.counter_writen >=7):
             s.counter_writen =1
             return
            return  # Exit the function early if exercise succeeds
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
        print("Step 1: Lifting arms to 90 degrees")
        self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)  # Left shoulder to 90 degrees
        self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)  # Right shoulder to -90 degrees
        time.sleep(0.5)
        # Step 2: Bend elbows to a 90-degree angle
        print("Step 2: rotating arms to 90 degrees")
        self.poppy.l_arm_z.goto_position(90, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(-90, 1.5, wait=True)
        time.sleep(0.5)
        print("bending elbows")
        self.poppy.l_elbow_y.goto_position(0, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(0, 1.5, wait=True)
        time.sleep(0.5)
        print("returning to initial position")
        self.poppy.l_elbow_y.goto_position(90, 1.5, wait=False)
        self.poppy.r_elbow_y.goto_position(90, 1.5, wait=True)
        time.sleep(0.5)
        print("Step 2: rotating arms to 0 degrees")
        self.poppy.l_arm_z.goto_position(0, 1.5, wait=False)
        self.poppy.r_arm_z.goto_position(0, 1.5, wait=True)
        time.sleep(0.5)
        print("last step: Lifting arms to 0 degrees")
        self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)  # Left shoulder to 90 degrees
        self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)  # Right shoulder to -90 degrees
        time.sleep(0.5)
        if s.have_voice:
            say(s.counter_writen)
            s.counter_writen = 1+s.counter_writen
        else:
            is_saying = self.what_to_say(s.counter_writen)
            s.screen.switch_frame(is_saying)
            s.counter_writen = 1+s.counter_writen

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
        if s.robot_count and s.have_voice==True:
              say(str(counter + 1))
              time.sleep(1)
        if s.robot_count and s.have_voice!=True:
              s.screen.switch_frame(self.what_to_say(str(counter + 1)))

    # EX2 - Bend Elbows
    def bend_elbows(self, counter):
        self.poppy.r_arm[3].goto_position(-60, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(-60, 1.5, wait=True)
        time.sleep(1.5)
        self.poppy.r_arm[3].goto_position(85, 1.5, wait=False)
        self.poppy.l_arm[3].goto_position(85, 1.5, wait=True)
        if s.robot_count and s.have_voice==True:
            say(str(counter + 1))
        time.sleep(1.4)
        if s.robot_count and s.have_voice!=True:
            s.screen.switch_frame(self.what_to_say(str(counter + 1)))
    

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
        if s.robot_count and s.have_voice==True:
            say(str(counter + 1))
        time.sleep(1)
        if s.robot_count and s.have_voice!=True:
            s.screen.switch_frame(self.what_to_say(str(counter + 1)))
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
        if s.robot_count and s.have_voice ==True:
            say(str(counter + 1))
        time.sleep(1)
        if s.robot_count and s.have_voice!=True:
            s.screen.switch_frame(self.what_to_say(str(counter + 1)))
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
        if s.robot_count and s.have_voice==True:
            say(str(counter + 1))
        time.sleep(1)
        if s.robot_count and s.have_voice!=True:
            s.screen.switch_frame(self.what_to_say(str(counter + 1)))
        if counter >= s.rep-1 or s.success_exercise:  # need to change it to constant
            self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
            self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
            self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
            self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            self.poppy.r_shoulder_x.goto_position(0, 1.5, wait=False)

    # EX5 - open and close arms 90 - one hand
    def open_and_close_arms_90_one_hand(self, counter):
        if counter == 0:
            if s.one_hand == 'right':  # mirror demo
                self.poppy.l_shoulder_y.goto_position(-90, 1.5, wait=False)
                self.poppy.l_elbow_y.goto_position(0, 1.5, wait=False)
            else:
                self.poppy.r_shoulder_y.goto_position(-90, 1.5, wait=True)
                self.poppy.r_elbow_y.goto_position(0, 1.5, wait=True)
        if s.one_hand == 'right':  # mirror demo
            self.poppy.l_shoulder_x.goto_position(90, 1, wait=False)
            time.sleep(1.8)
            self.poppy.l_shoulder_x.goto_position(0, 1, wait=False)
        else:
            self.poppy.r_shoulder_x.goto_position(-90, 1, wait=True)
            time.sleep(1.8)
            self.poppy.r_shoulder_x.goto_position(0, 1, wait=True)
        if s.robot_count:
            say(str(counter + 1))
        time.sleep(1)
        if counter >= s.rep-1 or s.success_exercise:  # TODO - Change to something that works if it finished before 8 repetitions.
            if s.one_hand == 'right':  # mirror demo
                self.poppy.l_elbow_y.goto_position(90, 1.5, wait=True)
                self.poppy.l_shoulder_y.goto_position(0, 1.5, wait=False)
                self.poppy.l_shoulder_x.goto_position(0, 1.5, wait=False)
            else:
                self.poppy.r_elbow_y.goto_position(90, 1.5, wait=False)
                self.poppy.r_shoulder_y.goto_position(0, 1.5, wait=True)
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
        if s.robot_count and s.have_voice==True:
            say(str(counter + 1))
        time.sleep(1)
        if s.robot_count and s.have_voice!=True:
            s.screen.switch_frame(self.what_to_say(str(counter + 1)))
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

