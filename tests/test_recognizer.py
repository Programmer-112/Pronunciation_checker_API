import pytest
from recognizer import Recognizer

audio_path = "tests/audio/iloveyou.wav"
def test_process_audio_valid():
    recog = Recognizer()
    # this file must exist and contain clear speech
    result = recog.process_audio(audio_path)
    assert isinstance(result, str)
    assert len(result) > 0   # should return some recognized text
    assert (result == "i love you")

def test_process_audio_invalid_path():
    recog = Recognizer()
    # non-existent file should raise FileNotFoundError
    with pytest.raises(FileNotFoundError):
        recog.process_audio("tests/audio/does_not_exist.wav")
