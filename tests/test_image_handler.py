import piexif
import pytest

from rmeta_core.handlers.image_handler import scrub


def test_scrub_removes_exif(dirty_jpg):
    before = piexif.load(str(dirty_jpg))
    assert before["0th"].get(piexif.ImageIFD.Artist) == b"MetaMaker"

    scrub(str(dirty_jpg))

    after = piexif.load(str(dirty_jpg))
    assert not any(after[ifd] for ifd in ("0th", "Exif", "GPS", "1st"))


def test_scrub_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        scrub("does-not-exist.jpg")


def test_scrub_unsupported_extension_raises(tmp_path):
    bogus = tmp_path / "dirty.bmp"
    bogus.write_bytes(b"not a real image")
    with pytest.raises(ValueError):
        scrub(str(bogus))
