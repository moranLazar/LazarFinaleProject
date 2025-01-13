import os
import pandas as pd
def __init__():

    # classes pointers
    global training
    global camera
    global robot
    global screen

    global participant_code
    global excel_workbook
    global ex_list

    # training variables
    global exercise_amount
    global rep
    global req_exercise
    global finish_workout
    global waved
    global success_exercise
    global calibration
    global poppy_done
    global camera_done
    global robot_count
    global try_again # Adaptive scenario - successful performance
    global robot_rep # number of repetition of the robot
    global team #if he started with interaction malfunction first and adaptive explenation he is team 1,
                         #if he started with interaction malfunction first he is 2 
                                       # if he started with hardware malfunction first and adaptive explanation, he is team 3,
                                          #  if he started with hardware malfunction first he is team 4
    global have_voice 
    global Fake_speaker ### change if it needed

    # audio variables
    global audio_path

    # screen variables
    global picture_path

    global camera_num

    # adaptation
    global adaptation_model
    global adaptive
    global performance_class
    global corrective_feedback
    global one_hand

    def is_speaker_Active(self,path):
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
        return False