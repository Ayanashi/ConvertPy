import os
from convert import convert_to_audio


def test_convert_to_audio(tmp_path):
    """
    Test
    """
    # File
    input_file = tmp_path / "video.mp4"
    input_file.write_text("dummy content")

    output_file = tmp_path / "audio.mp3"

    # Conversion
    convert_to_audio(str(input_file), str(output_file))

    # Output check
    assert output_file.exists()
