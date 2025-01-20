import time
import Settings as s
import Excel
from Camera import Camera
from Poppy import Poppy
from Audio import Audio
from Training import Training
from Screen import Screen, FullScreenApp
from PIL import Image, ImageTk
import pickle
import datetime


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
# TODO add more exercises
# TODO adaptive framework
# TODO GUI
# delay between exercises
if __name__ == '__main__':
    s.camera_num = 0  # 0 - webcam, 2 - second USB in maya's computer

    # Audio variables initialization
    language = 'Hebrew'
    gender = 'Male'
    s.audio_path = 'audio files/' + language + '/' + gender + '/'
    s.picture_path = 'audio files/' + language + '/' + gender + '/'
    # s.str_to_say = ""
    current_time = datetime.datetime.now()
    s.participant_code = str(current_time.day) + "." + str(current_time.month) + " " + str(current_time.hour) + "." + \
                         str(current_time.minute) + "." + str(current_time.second)

    # Training variables initialization
    s.exercise_amount = 5
    s.rep = 3
    s.req_exercise = ""
    s.req_exercise_inter=1
    s.finish_workout = False
    s.waved = False
    s.success_exercise = False
    s.calibration = False # False to have calibration session, True to not have
    s.training_done = False
    s.poppy_done = False
    s.camera_done = False
    s.robot_count = True
    s.try_again = False
    s.team = 1
    s.saying_inter=False
    s.counter_writen =1 
    s.have_voice = True
    # Excel variable
    Excel.create_workbook()
    s.ex_list = []
    # Create all components
    s.camera = Camera()
    s.training = Training()
    s.robot = Poppy()
    s.Fake_speaker= False ## it will still be false, but its need to get output from port

    # Adaptation variables
    s.adaptive = True
    s.corrective_feedback = False
    s.one_hand = False
    if s.adaptive:
        s.adaptation_model_name = 'performance_evaluation_model'
        s.performance_class = {}
        # s.adaptation_model = pickle.load(open(f'{adaptation_model_name}.sav', 'rb'))

    # Start all threads
    s.camera.start()
    s.training.start()
    s.robot.start()
    s.screen = Screen()
    image1 = Image.open('Pictures//icon.jpg')
    s.screen.tk.call('wm', 'iconphoto', s.screen._w, ImageTk.PhotoImage(image1))
    app = FullScreenApp(s.screen)
    s.screen.mainloop()

