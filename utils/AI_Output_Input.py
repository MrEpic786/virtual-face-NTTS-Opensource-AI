import pyttsx3
import speech_recognition as sr
import webbrowser
from pyautogui import keyDown
from elevenlabslib import *
from pydub import AudioSegment
from utils.AI_Videos import *
import threading
from dotenv import load_dotenv
import os
import audiostack
import winsound
import requests
import urllib.request

AudioSegment.converter = "C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffmpeg = "C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin\ffmpeg.exe"

Voice = "Bella" # Type Of Voice
DefVoiceRate = 170 #Speed Of Voice
speakingEnergy = 500
pause_threshold = 0.50
listeningLanguage = 'en-IN'
# load values from the .env file if it exists
load_dotenv()
elevenLabsApiKeys = os.getenv("ELEVENLABS_API_KEY")
audiostack.api_key = os.getenv("ELEVENLABS_API_KEY")

from elevenlabslib import ElevenLabsUser
user = ElevenLabsUser(elevenLabsApiKeys)

# First Define Settings
class FunctionSetting:
    global SpeakingEnergy
    def SpeakingEnergy(EnergyRate):
        global speakingEnergy
        speakingEnergy = EnergyRate

    global listeningLanguageChange
    def listeningLanguageChange(languageCode):
        global listeningLanguage
        listeningLanguage = languageCode

    global pauseThreshold
    def pauseThreshold(pause_threshold_rate):
        global pause_threshold
        pause_threshold = pause_threshold_rate


    global voiceSpeed
    def voiceSpeed(voiceSpeed):
        global DefVoiceRate
        DefVoiceRate = voiceSpeed

    global voiceType
    def voiceType(VoiceType):
       global Voice
       Voice = VoiceType

    global ConvertNumToVolume
    def ConvertNumToVolume(v):#100
        if v%2 == 0:
            Ans = v/2
            return int(Ans)
        elif v%2 == 1:
            c = v-1
            if c%2 == 0:
                Ans = c/2
                return int(Ans)
            else:
                print("Error!!")


class Function:

    # With Pyttsx3 
    global speakByPytts
    def speakByPytts(audio): 
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', DefVoiceRate)
        engine.say(audio)
        startSpeakingVoice()
        engine.runAndWait()
        endSpeakingVideo()

    global speakNepaliByAudioStack
    def speakNepaliByAudioStack(text):
        scriptText = text
        script = audiostack.Content.Script.create(
        scriptText=scriptText,
        )
        tts = audiostack.Speech.TTS.create(
        scriptItem=script,
        voice="Suman")

        encoder = audiostack.Speech.TTS.get(tts.speechId)

        encoder.download(fileName=encoder.speechId)
        startSpeakingVoice()
        winsound.PlaySound(encoder.speechId+"_1_of_1.wav", winsound.SND_FILENAME)
        # encoder.delete(encoder.speechId)
        endSpeakingVideo()
        if os.path.exists(encoder.speechId+"_1_of_1.wav"):
            os.remove(encoder.speechId+"_1_of_1.wav") # one file at a time

    global speakHindiByPlayHt
    def speakHindiByPlayHt(text):
        headers = {'X-User-ID': '<USER ID HERE>',
        'Authorization': '<AUTHORIZATION HERE>',
        "User-agent": "Mozilla/5.0"
        }
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        filename = 'speech.wav'

        payload = {
        "voice": "hi-IN-Wavenet-D",
        "content": [text]
        }

        response = requests.post("https://play.ht/api/v1/convert", json=payload, headers=headers)

        transcriptionId = response.json()["transcriptionId"]

        x = requests.get("https://play.ht/api/v1/articleStatus?transcriptionId="+transcriptionId,headers=headers)


        urllib.request.urlretrieve(x.json()["audioUrl"], filename)
        startSpeakingVoice()
        winsound.PlaySound(filename, winsound.SND_FILENAME)
        endSpeakingVideo()
        if os.path.exists(filename):
            os.remove(filename) # one file at a time



    # With ElevenLabs 

    global speakEnglishByElevenLabs
    def speakEnglishByElevenLabs(text):
        voice = user.get_voices_by_name(Voice)[0]
        voice.generate_and_play_audio(text, playInBackground=False,
        onPlaybackStart=startSpeakingVoice ,onPlaybackEnd=endSpeakingVideo)
        


    global speak
    def speak(text):
        if listeningLanguage == 'en-IN':
            speakEnglishByElevenLabs(text)
            # speakByPytts(text)
        elif listeningLanguage == 'hi-In':
            speakHindiByPlayHt(text)
        elif listeningLanguage == 'ne-NP':
            speakNepaliByAudioStack(text)
        else:
            speakByPytts(text)

    global initializeAiVideoFun
    def initializeAiVideoFun():
            t1 = threading.Thread(target=initializeAiVideo, args=())
            t1.start()

    global takeCommand
    def takeCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listing....")
            r.pause_threshold = pause_threshold
            r.energy_threshold = speakingEnergy
            audio = r.listen(source)
            
        try:
            print("working on it...")
            query = r.recognize_google(audio, language=listeningLanguage)
            print(f"User said: {query}\n")

        except Exception as e:
            print("say that again please...")
            return "None"
        return query

    global VolumeMute
    def VolumeMute():
        keyDown("volumemute") #Visit  https://pyautogui.readthedocs.io/en/latest/keyboard.html#keyboard-keys

    global VolumeUp
    def VolumeUp(volume):
        VolumeUpPerc = ConvertNumToVolume(volume)
        for j in range(27):
            keyDown("volumedown")
        for i in range(VolumeUpPerc):
            keyDown("volumeup")

    global VolumeDown
    def VolumeDown():
        for i in range(5):
            keyDown("volumedown")

    global OpenWebsite
    def OpenWebsite(link):
        webbrowser.open(link)



if __name__ == "__main__":
    initializeAiVideoFun()
    speak("hi hello! How are you?")
    # VolumeUp(4)
    # OpenWebsite("https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley")
