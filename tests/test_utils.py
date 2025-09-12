from utils import sanitize_filename

def test_sanitize_filename_basic():
    input_name = "te*st:fi|le?.mp3"
    result = sanitize_filename(input_name)
    for char in "*:|?":
        assert char not in result

def test_sanitize_filename_empty():
    assert sanitize_filename("") == ""
