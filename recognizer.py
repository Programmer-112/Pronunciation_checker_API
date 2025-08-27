import speech_recognition as sr

class Recognizer:
     def process_audio(self, audio_path):
            recog = sr.Recognizer()
            try:
                with sr.AudioFile(audio_path) as src:
                    audio_data = recog.record(src)
                    
                    return recog.recognize_google(audio_data).lower()
            except sr.UnknownValueError:
                 return ""