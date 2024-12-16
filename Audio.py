import threading
import Settings as s
import winsound
from pygame import mixer
import time


class Audio(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print ("AUDIO INITIALIZATION")

    def run(self):
        while not s.finish_workout:
            if s.str_to_say!="":
                self.say_no_wait(s.str_to_say)
                print("tts says: ", s.str_to_say)
                s.str_to_say = ""
        print ("AUDIO DONE")

    def say1(self, str_to_say):
        if (str_to_say != ""):
            winsound.PlaySound(s.audio_path+str_to_say+'.wav', winsound.SND_FILENAME)


def say(str_to_say):
    '''
    str_to_say = the name of the file
    This function make the robot say whatever there is in the file - play the audio (paralelly)
    :return: audio
    '''
    try:
        mixer.init()
        sound = mixer.Sound(s.audio_path+str_to_say+'.wav')
        audio_length = sound.get_length()
        sound.play()
        time.sleep(audio_length-1)
    except Exception as e:
        print(f"error sound not found: {e}")

if __name__ == '__main__':
    language = 'Hebrew'
    gender = 'male'
    s.audio_path = 'audio files/' + language + '/' + gender + '/'

    # audio = Audio()
    # audio.say('raise arms forward')
    say("open_and_close_arms_90_one_hand_false")
    time.sleep(5)
