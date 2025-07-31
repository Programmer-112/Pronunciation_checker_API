import os

from scorer import Scorer

AUDIO_DIR = (os.path.join(os.path.dirname(__file__), 'audio'))

scr = Scorer()
def test_perfect_pronunciation():
    audio_path = os.path.join(AUDIO_DIR, 'rabbit.wav')
    print(audio_path)
    s, _ = scr.score(audio_path, "rabbit")
    assert s >= 0.9


def test_bad_pronunciation():
    audio_path = os.path.join(AUDIO_DIR, 'ribbit.wav')
    s, _ = scr.score(audio_path, "rabbit")
    assert s < 0.7


def test_perfect_sentence():
    audio_path = os.path.join(AUDIO_DIR, 'iloveyou.wav')
    s, _ = scr.score(audio_path, "i love you")
    assert s >= 0.9


def test_bad_sentence():
    audio_path = os.path.join(AUDIO_DIR, 'iloveyou.wav')
    s, _ = scr.score(audio_path, "i loath you")
    assert s < 0.7


def test_good_paragraph():
    audio_path = os.path.join(AUDIO_DIR, 'paragraph.wav')
    text = """A computer is a machine that can be programmed to automatically carry out sequences of arithmetic "
                  "or logical operations. Modern digital electronic computers can perform generic sets of
                   operations known as programs, which enable computers to perform a wide range of tasks."""

    s, _ = scr.score(audio_path, text)
    assert s >= 0.85
