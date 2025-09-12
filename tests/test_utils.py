import pytest
from utils import sanitize_filename

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
