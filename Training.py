import threading
import time
import Settings as s
import Excel
import random
from Audio import say
import Screen as screen
import os
import pandas as pd
from Screen import EyesPage,goodbye,Alert,continue_inter,finished_impossible_ex_good,raise_arms_bend_elbows,open_and_close_arms,raise_arms_forward,bend_elbows,impossible_EX,Continue,Why_inter,What_inter,Why_Hardware,What_Hardware,How_Hardware
######### this is the correct one lazars 2


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
        self.explaining_Exit_Movment("check_hello_wave")
        time.sleep(2.5)
        print("Training: finish waving")
        self.warm_up()
        say('lets start')
        time.sleep(2.5)
        print("Training: finish warmup")
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

    def explaining_Exit_Movment(self,name, hand=''):
        say('how_inter')
        time.sleep(1) ######## we need to find out what is the right time with this specific Audio
        print("explaining how to make the robot go next")
        self.run_exercise("check_hello_wave") 
        print("showing the right motion")
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
        exercise_names = ["raise_arms_horizontally","impossible_EX_Adaptive",  "raise_arms_bend_elbows","bend_elbows", "open_and_close_arms" ]
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
        exercise_names = ["raise_arms_horizontally","impossible_EX", "raise_arms_bend_elbows", "bend_elbows", "open_and_close_arms"]
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
        if s.have_voice:
         say('goodbye')
        else:
         s.screen.switch_frame(goodbye) #screen goodbye
        s.finish_workout = True
        Excel.success_worksheet()
        Excel.close_workbook()
        time.sleep(10)
        s.screen.quit()
        print("TRAINING DONE")
    
    def impossible_EX_func(self):
        print("Waiting for 2 minutes before exiting")
        for _ in range(120):  # Wait for 2 minutes in 1-second intervals
              s.camera.waiving()
              if s.waved==True :  # Continuously check for hello_wave this is the situation when he does have voice and the user manage to solve it
                if(s.have_voice==True):
                 say('finished_impossible_ex_good')
                 time.sleep(3)
                 print("Hello_wave motion detected during final waiting period. Ending impossible_EX.")
                 return
                else:
                 s.screen.switch_frame(finished_impossible_ex_good)
                 time.sleep(2)
                 print("Hello_wave motion detected during final waiting period. Ending impossible_EX.")
                 return  #this situation is when he does have voice and the user didnt manage to solve the  inter problem
        if(s.have_voice==True):
                 say('continue_inter')
                 print("Hello_wave motion was not detected during final waiting period. Ending impossible_EX.")
                 return
        else: # the user faild the hardware problem 
                time.sleep(2)
                s.screen.switch_frame(continue_inter)
                time.sleep(2)
                print("Hello_wave motion was not detected during final waiting period. Ending impossible_EX.")
                return

    def impossible_EX_Adaptive_func(self):
        print("Waiting for 1 minute before issuing 'what_inter'")
        if(s.have_voice==True):
                say('what_inter')
                time.sleep(3)
        else:
                time.sleep(23)
                s.screen.switch_frame(What_inter)
                time.sleep(2)
        
        for _ in range(60):  # Wait for 1 minute in 1-second intervals
                s.camera.waiving()
                if s.waved==True and s.have_voice==True :  # Continuously check for hello_wave
                 say('finished_impossible_ex_good')
                 print("Hello_wave motion detected during final waiting period. Ending impossible_EX.")
                 return
                if s.waved==True and s.have_voice!=True :  # Continuously check for hello_wave
                    time.sleep(2)
                    s.screen.switch_frame(finished_impossible_ex_good)
                    time.sleep(2)
                    return
                time.sleep(1)
        print("Waiting for another 1 minute before issuing 'why_inter'")
        if(s.have_voice==True):
                say('why_inter')
                time.sleep(3)
        else:
                time.sleep(23)
                s.screen.switch_frame(Why_inter)
                time.sleep(2)
        for _ in range(60):  # Wait for another 1 minute in 1-second intervals
                s.camera.waiving()
                if s.waved==True and s.have_voice==True:  # Continuously check for hello_wave
                  say('finished_impossible_ex_good')
                  print("Hello_wave motion detected during final waiting period. Ending impossible_EX.")
                  return
                if s.waved==True and s.have_voice!=True:
                  if s.waved==True :  # Continuously check for hello_wave
                    s.screen.switch_frame(finished_impossible_ex_good)
                    
                    return
        if      s.waved!=True and s.have_voice==True:
                  say('continue_inter')
                  time.sleep(3)
                  print("Hello_wave motion was not detected during final waiting period. Ending impossible_EX.")
                  return
        else:
                    s.screen.switch_frame(continue_inter)
                    print("Hello_wave motion was not detected during final waiting period. Ending impossible_EX.")
                    return
    def is_speaker_Active(self, path):
        try:
        # Check if the file exists
         if os.path.exists(path):
            pd.read_excel(path)  # Attempt to import the file
            print("File imported successfully!")
            return True
         else:
            print(f"File does not exist at: {path}")
            return False
        except Exception as e:
         print(f"Error while trying to import the file: {e}")
        return True            
    def run_exercise(self, name, hand=''):
        s.success_exercise = False
        print("TRAINING: Exercise ", name, " start")
        if name=="impossible_EX":
            self.impossible_EX_func()
        if name=="impossible_EX_Adaptive":
            self.impossible_EX_Adaptive_func()
        if(name=="bend_elbows"):
            s.Have_voice=False
            self.Time_to_check_voice(s.team,s.have_voice,s.Fake_speaker)
            if s.Have_voice==True:
                 say(name+hand)
                 time.sleep(3)  # Delay the robot movement after the audio is played
            else :
                s.screen.switch_frame(bend_elbows)
                time.sleep(2)
            time.sleep(3)  # Delay the robot movement after the audio is played
        elif(s.have_voice==True and name!="bend_elbows" and name !="impossible_EX" and name !="impossible_EX_Adaptive"):
            say(name+hand)
            time.sleep(3)  # Delay the robot movement after the audio is played
        elif(s.have_voice!=True and name!="bend_elbows" and name !="impossible_EX" and name !="impossible_EX_Adaptive"):
            self.What_To_wirte (name)
            time.sleep(2)
        s.req_exercise = name
        while s.req_exercise == name:
            time.sleep(0.001)  # Prevents the MP to stuck
        if s.success_exercise and  s.have_voice==True:
            say(self.random_encouragement())
        print("TRAINING: Exercise ", name, " done")
        if s.success_exercise and  s.have_voice!=True:
           s.screen.switch_frame(self.random_encouragement_write())
        time.sleep(1)
    
    def random_encouragement_write(self):
        enco = ["well_done", "very_good", "excellent"]
        return random.choice(enco)

    def random_encouragement(self):
        enco = ["well done", "very good", "excellent"]
        return random.choice(enco)
    
    def What_To_wirte (self,name):
        if(name=='raise_arms_bend_elbows'):
            s.screen.switch_frame(raise_arms_bend_elbows)
        if(name=='impossible_EX' or name=='impossible_EX_Adaptive'):
            s.screen.switch_frame(impossible_EX)
        if(name=='open_and_close_arms'):
            s.screen.switch_frame(open_and_close_arms)
        if(name=='raise_arms_forward'):
            s.screen.switch_frame(raise_arms_forward)
    
def Time_to_check_voice(self, team, have_voice, Fake_speaker):
    csv_path = r"D:\פרוייקט גמר\project_bullshit_on_its_way.xlsx"  # Path to check speaker

    # Start with the Alert frame
    s.screen.switch_frame(Alert)
    time.sleep(15)

    if team in [1, 3]:  # Groups with multi-stage hardware checks
        hardware_stages = [
            (How_Hardware, "how Finished hardware problem"),
            (What_Hardware, "what Finished hardware problem"),
            (Why_Hardware, "why Finished hardware problem"),
            (Continue, "Finished hardware check, no solution found"),
        ]

        for frame, message in hardware_stages[:-1]:
            s.screen.switch_frame(frame)
            time.sleep(2)

            print(f"Checking for speaker activity during '{frame.__name__}'")
            for _ in range(40):  # Check for 40 seconds in 1-second intervals
                s.Fake_speaker = self.is_speaker_Active(csv_path)
                time.sleep(1)
                if s.Fake_speaker:  # Speaker detected
                    s.have_voice = True
                    print(message)
                    say("Fix_Hardware_Good")
                    s.screen.switch_frame(EyesPage)
                    return have_voice  # Exit early if resolved

        # If no speaker detected after all stages
        s.screen.switch_frame(hardware_stages[-1][0])  # Continue frame
        print(hardware_stages[-1][1])
        time.sleep(2)
        s.have_voice = False
        return have_voice

    elif team in [2, 4]:  # Groups with single-stage (120s) hardware checks
        s.screen.switch_frame(How_Hardware)
        print("Team 2 or 4: Checking hardware for 120 seconds in 'How_Hardware'")
        for _ in range(120):  # Check for 120 seconds in 2-second intervals
            s.Fake_speaker = self.is_speaker_Active(csv_path)
            time.sleep(2)
            if s.Fake_speaker:  # Speaker detected
                s.have_voice = True
                say("Fix_Hardware_Good")
                print("Finished hardware problem")
                s.screen.switch_frame(EyesPage)
                return s.have_voice

        # If no speaker detected after 120 seconds
        s.screen.switch_frame(Continue)
        print("No hardware solution found after 120 seconds. Showing 'Continue'.")
        time.sleep(2)
        s.have_voice = False
        return have_voice
     
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
