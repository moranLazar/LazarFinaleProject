import threading
import time
import Settings as s
import Excel
import random
from Audio import say


class Training(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("TRAINING START")
        self.run_exercise("hello_waving")
        print("Training: start waving")
        while not s.waved:
            time.sleep(0.00000001)  # Prevents the MP to stuck
            continue
        s.waved = False # set as False again for future
        if not s.calibration:
            print("Training: Calibration")
            s.camera.init_position()
            while not s.calibration:
                time.sleep(0.00000001)
                continue
        time.sleep(3)
        say('lets start')
        time.sleep(2.5)
        print("Training: finish waving")
        s.poppy_done = False  # AFTER HELLO
        s.camera_done = False  # AFTER HELLO
        if s.adaptive:
            self.adaptive_training_session()
        else:
            self.training_session()

        self.finish_workout()

    def adaptive_training_session(self):
        exercise_names = ["raise_arms_horizontally", "bend_elbows"]
        for e in exercise_names:
            time.sleep(2)
            self.run_exercise(e)
            while (not s.poppy_done) or (not s.camera_done):
                print("not done")
                time.sleep(1)
            s.poppy_done = False
            s.camera_done = False

        right_values = [value['right'] for value in s.performance_class.values()]
        left_values = [value['left'] for value in s.performance_class.values()]
        if sum(right_values) > 1.1 and sum(left_values) > 1.1:
            print("problem in both hands!")
            s.corrective_feedback = True
        elif sum(right_values) > 1.1:  # In the middle of the exercise provide corrective feedback
            # (for example: try to raise your hand more),
            print("problem in right hand!")
            s.one_hand = 'right'
            s.corrective_feedback = True
            say("adaptive_focused_right")
        elif sum(left_values) > 1.1:  # problem in left hand!
            print("problem in left hand!")
            s.one_hand = 'left'
            s.corrective_feedback = True
            say("adaptive_focused_left")
        else:
            print("no problems!")  # add try again if not succeeded
            s.robot_count = False
            s.try_again = True
            say("adaptive_bothgood")

        exercise_names = ["raise_arms_bend_elbows", "open_and_close_arms",
                          "open_and_close_arms_90", "raise_arms_forward"]
        if s.one_hand == False:
            for e in exercise_names:
                time.sleep(2)  # wait between exercises
                self.run_exercise(e)
                while (not s.poppy_done) or (not s.camera_done):
                    print("not done")
                    time.sleep(1)
                if s.try_again == True and s.success_exercise == False: # for
                    print("TRAINING: Try Again")
                    time1 = time.time()
                    time2 = 0
                    s.req_exercise = "hello_waving"
                    time.sleep(2)
                    print("TRAINING: wait for trying again")
                    while not s.waved and (time2 - time1 < 15):
                        time.sleep(0.00000001)  # Prevents the MP to stuck
                        time2 = time.time()
                        continue
                    s.req_exercise = ""
                    if s.waved:
                        print(f"TRAINING: try again exercise {e}")
                        s.waved = False  # set as False again for future
                        self.run_exercise(e)
        else: # training for one hand
            print(f"Training focused on {s.one_hand} hand")
            one_hand_exercise_names = ["raise_arms_bend_elbows_one_hand", "open_and_close_arms_one_hand",
                                       "open_and_close_arms_90_one_hand", "raise_arms_forward_one_hand"] #to do - add exercises
            for e in one_hand_exercise_names:
                time.sleep(2)  # wait between exercises
                self.run_exercise(e, "_"+s.one_hand)
                while (not s.poppy_done) or (not s.camera_done):
                    print("not done")
                    time.sleep(1)

        #TODO - ADD HERE THE TWO EXERCISES OF THE BEGNING AGAIN.
        s.one_hand = False
        print("TRAINING: repeat_first_exercises")
        say("repeat_first_exercises")
        exercise_names = ["raise_arms_horizontally", "bend_elbows"]
        for e in exercise_names:
            time.sleep(2)
            self.run_exercise(e)
            while (not s.poppy_done) or (not s.camera_done):
                print("not done")
                time.sleep(1)
            s.poppy_done = False
            s.camera_done = False

    def training_session(self):
        print("Training: start exercises")
        # TODO - adding random choice of exercises.
        exercise_names = ["raise_arms_horizontally", "bend_elbows", "raise_arms_bend_elbows", "open_and_close_arms",
                          "open_and_close_arms_90", "raise_arms_forward"]
        for e in exercise_names:
            time.sleep(2) # wait between exercises
            self.run_exercise(e)
            while (not s.poppy_done) or (not s.camera_done):
                print("not done")
                time.sleep(1)

    def finish_workout(self):
        say('goodbye')
        s.finish_workout = True
        Excel.success_worksheet()
        Excel.close_workbook()
        time.sleep(10)
        s.screen.quit()
        print("TRAINING DONE")

    def run_exercise(self, name, hand=''):
        s.success_exercise = False
        print("TRAINING: Exercise ", name, " start")
        say(name+hand)
        # time.sleep(3)  # Delay the robot movement after the audio is played
        s.req_exercise = name
        while s.req_exercise == name:
            time.sleep(0.001)  # Prevents the MP to stuck
        if s.success_exercise:
            say(self.random_encouragement())
        print("TRAINING: Exercise ", name, " done")
        time.sleep(1)

    def random_encouragement(self):
        enco = ["well done", "very good", "excellent"]
        return random.choice(enco)


if __name__ == "__main__":
    # Create all components
    from Camera import Camera
    from Poppy import Poppy

    s.camera = Camera()
    s.robot = Poppy()
    language = 'Hebrew'
    gender = 'Male'
    s.audio_path = 'audio files/' + language + '/' + gender + '/'
    s.finish_workout = False
    s.rep = 8 #todo change to 8
    s.req_exercise = ""
    s.robot_count = True

    # Adaptation variables
    s.adaptive = True
    s.corrective_feedback = True
    s.one_hand = False
    s.robot_rep = 0
    if s.adaptive:
        s.adaptation_model_name = 'performance_evaluation_model'
        s.performance_class = {}
    s.camera.start()
    s.robot.start()

    t = Training()
    t.run_exercise("open_and_close_arms_90")