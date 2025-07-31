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

    def score(self, audio_path, target):
        recog, twords = sr.Recognizer(), target.lower().split()
        with sr.AudioFile(audio_path) as src:
            transcript = recog.recognize_google(recog.record(src)).lower()

        ph_tr  = sum((self.phones(w) for w in transcript.split()), [])
        ph_tgt = sum((self.phones(w) for w in twords), [])
        return self.calculate_score("".join(ph_tgt), "".join(ph_tr)), transcript

