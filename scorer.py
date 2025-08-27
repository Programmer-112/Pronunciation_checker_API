import asyncio
import Levenshtein, pronouncing, speech_recognition as sr


class Scorer:
    def __init__(self):
        pass

    def phones(self, word):  # ARPAbet phones for a word
        lst = pronouncing.phones_for_word(word.lower())
        return lst[0].split() if lst else []

    def calculate_score(self, expected, target):
        dist = Levenshtein.distance(expected, target)
        return max(0, 1 - dist / max(len(expected), 1))
    
    def process_audio(self, audio_path):
            recog = sr.Recognizer()
            with sr.AudioFile(audio_path) as src:
                audio_data = recog.record(src)
                
                return recog.recognize_google(audio_data).lower()

    async def async_score(self, audio_path, target):
        twords = target.lower().split()
        transcript = await asyncio.to_thread(self.process_audio, audio_path)
        ph_tr = sum((self.phones(w) for w in transcript.split()), [])
        ph_tgt = sum((self.phones(w) for w in twords), [])
        score = self.calculate_score("".join(ph_tgt), "".join(ph_tr))
        score = round(score, 2)

        return score, str(transcript)
    