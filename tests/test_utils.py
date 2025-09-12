import pytest
from utils import sanitize_filename

<<<<<<< HEAD
def test_sanitize_filename():
    """
    Test filename sanitization.
    """
    # Basic sanitization
    assert sanitize_filename("my file.mp4") == "my_file.mp4"
    # Remove invalid characters
    assert sanitize_filename("video@#$.mp3") == "video__.mp3"
    # Already valid
    assert sanitize_filename("audio_file.wav") == "audio_file.wav"
||||||| parent of e4f1021 (minor updates and fix)
def test_sanitize_filename_basic():
    input_name = "te*st:fi|le?.mp3"
    result = sanitize_filename(input_name)
    for char in "*:|?":
        assert char not in result

def test_sanitize_filename_empty():
    assert sanitize_filename("") == ""
=======

def test_sanitize_filename_basic():
    input_name = "te*st:fi|le?.mp3"
    result = sanitize_filename(input_name)
    for char in "*:|?":
        assert char not in result


def test_sanitize_filename_empty():
    assert sanitize_filename("") == ""
>>>>>>> e4f1021 (minor updates and fix)
