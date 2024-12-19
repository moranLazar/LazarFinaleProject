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
        self.explaining_Exit_Movment()
        time.sleep(2.5)
        self.warm_up()
        say('lets start')
        time.sleep(2.5)
        print("Training: finish waving")
        s.poppy_done = False  # AFTER HELLO
        s.camera_done = False  # AFTER HELLO
        if s.team==1:
            self.training_session_interaction_first_adaptive()
        if s.team==2:
            self.training_session_interaction_first()
        if s.team==3:
            self.training_session_hardware_first_adaptive()
        if s.team==4:
            self.training_session_hardware_first()
        self.finish_workout()

    def warm_up(self):
        say('start_warm_up')
        print("Training: start exercises")
        # TODO - adding random choice of exercises.
        exercise_names = ["open_and_close_arms_90","raise_arms_forward"]
        for e in exercise_names:
            time.sleep(2) # wait between exercises
            self.run_exercise(e)
            while (not s.poppy_done) or (not s.camera_done):
                print("not done")
                time.sleep(1)
        say('end_warm_up')

    def explaining_Exit_Movment(self):
        say('how_inter')
        time.sleep(6) ######## we need to find out what is the right time with this specific Audio
        print("explaining how to make the robot go next")
        self.run_exercise("hello_waving") 
        print("showing the right motion")
        while not s.waved:
            time.sleep(0.00000001)  # Prevents the MP to stuck
            continue
        s.waved = False # set as False again for future
        time.sleep(3)
        say('very good') ###### change the command or record the right one 
        time.sleep(2.5)
        print("finished the explanation")
        s.poppy_done = False  # AFTER HELLO
        s.camera_done = False  # AFTER HELLO

    #people between 0-10
    def training_session_interaction_first_adaptive(self):
        print("Training: start exercises")
        # TODO - adding random choice of exercises.
        exercise_names = ["raise_arms_horizontally","impossible_EX_Adaptive", "bend_elbows", "raise_arms_bend_elbows", "open_and_close_arms", ]
        for e in exercise_names:
            time.sleep(2) # wait between exercises
            self.run_exercise(e)
            while (not s.poppy_done) or (not s.camera_done):
                print("not done")
                time.sleep(1)
    #people between 10-20
    def training_session_interaction_first(self):
        print("Training: start exercises")
        # TODO - adding random choice of exercises.
        exercise_names = ["raise_arms_horizontally","impossible_EX", "bend_elbows", "raise_arms_bend_elbows", "open_and_close_arms"]
        for e in exercise_names:
            time.sleep(2) # wait between exercises
            self.run_exercise(e)
            while (not s.poppy_done) or (not s.camera_done):
                print("not done")
                time.sleep(1)
    #people between 20-30
    def training_session_hardware_first_adaptive(self):
        print("Training: start exercises")
        # TODO - adding random choice of exercises.
        exercise_names = ["raise_arms_horizontally", "bend_elbows", "raise_arms_bend_elbows", "impossible_EX_Adaptive","open_and_close_arms"]
        for e in exercise_names:
            time.sleep(2) # wait between exercises
            self.run_exercise(e)
            while (not s.poppy_done) or (not s.camera_done):
                print("not done")
                time.sleep(1)
    #people between 30-40    
    def training_session_hardware_first(self):
        print("Training: start exercises")
        # TODO - adding random choice of exercises.
        exercise_names = ["raise_arms_horizontally", "bend_elbows", "raise_arms_bend_elbows","impossible_EX", "open_and_close_arms"]
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

    def run_exercise(self, name, hand='',):
        s.success_exercise = False
        print("TRAINING: Exercise ", name, " start")
        if(name=="bend_elbows"):
            s.Have_voice=False
            s.Time_to_check_voice(s.team,s.have_voice)
        if(self.have_voice==True and name!="bend_elbows"):
            say(name+hand)
            time.sleep(3)  # Delay the robot movement after the audio is played
        if(self.have_voice!=True and name!="bend_elbows"):
            s.switch_frame()
            time.sleep(2)
            s.What_To_wirte (name)
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
    
    def What_To_wirte (name):
        if (name=='bend_elbows'):
            s.bebend_elbows()
        if(name=='raise_arms_bend_elbows'):
            s.raise_arms_bend_elbows()
        if(name=='impossible_EX' or name=='impossible_EX_Adaptive'):
            s.impossible_EX()
        if(name=='open_and_close_arms'):
            s.open_and_close_arms()
        if(name=='raise_arms_forward'):
            s.raise_arms_forward()
            
    def Time_to_check_voice(team):
     s.switch_frame()
     time.sleep(2)
     s.How_HardWare()
     s.Alert()
     time.sleep(2)
     s.How_HardWare()
     print("Waiting for 1 minute before issuing 'what_inter'")
     if s.team == 1 or s.team == 3:
        for _ in range(40):  # Wait for 40 sec in 1-second intervals
            if s.Fake_speaker:  # Continuously check for port output
                say('Fix_Hardware_Good')
                print("Finished hardware problem")
                s.have_voice=True
                return    
        for _ in range(40):  # Wait for 40 sec in 1-second intervals
            s.switch_frame()
            time.sleep(2)
            s.What_Hardware()
            if s.s.Fake_speaker:  # Continuously check for port output
                say('Fix_Hardware_Good')
                print("Finished hardware problem")
                s.have_voice=True
                return    
        for _ in range(40):  # Wait for 40 sec in 1-second intervals
            s.switch_frame()
            time.sleep(2)
            s.Why_Hardware()
            if s.s.Fake_speaker:  # Continuously check for port output
                say('Fix_Hardware_Good')
                print("Finished hardware problem")
                s.have_voice=True
                return
        s.switch_frame()
        time.sleep(2)
        s.Continue()
        return
     else:
        for _ in range(120):  # Wait for 120 sec in 1-second intervals
            s.switch_frame()
            time.sleep(2)
            s.How_HardWare()
            if s.Fake_speaker:  # Continuously check for hello_wave
                say('Fix_Hardware_Good')
                print("Finished hardware problem")
                s.have_voice=True
                return
        s.switch_frame()
        time.sleep(2)
        s.Continue()
        return

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