from scorer import Scorer

scr = Scorer()
def test_perfect_pronunciation():
    s = scr.score("rabbit", "rabbit")
    assert s >= 0.9


def test_bad_pronunciation():
    s = scr.score("turtle", "rabbit")
    assert s < 0.7


def test_perfect_sentence():

    s = scr.score("i love you", "i love you")
    assert s >= 0.9


def test_bad_sentence():

    s = scr.score("i love you", "i loath you")
    assert s < 0.7


def test_good_paragraph():
    text = """A computer is a machine that can be programmed to automatically carry out sequences of arithmetic "
                  "or logical operations. Modern digital electronic computers can perform generic sets of
                   operations known as programs, which enable computers to perform a wide range of tasks."""

    s = scr.score(text, text)
    assert s >= 0.85
