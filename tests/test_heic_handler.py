import asyncio

import pytest

pillow_heif = pytest.importorskip("pillow_heif")
pillow_heif.register_heif_opener()

from PIL import Image  # noqa: E402

from rmeta_core.handlers.heic_handler import scrub  # noqa: E402


@pytest.fixture
def dirty_heic(tmp_path):
    path = tmp_path / "dirty.heic"
    img = Image.new("RGB", (32, 32), color="blue")
    heif_file = pillow_heif.from_pillow(img)
    heif_file.info["exif"] = b"Exif\x00\x00fake-exif-payload-marker"
    heif_file.save(str(path), quality=95)
    return path


def test_scrub_removes_exif(dirty_heic):
    before = pillow_heif.open_heif(str(dirty_heic))
    assert before.info.get("exif") is not None

    asyncio.run(scrub(str(dirty_heic)))

    after = pillow_heif.open_heif(str(dirty_heic))
    assert after.info.get("exif") is None


def test_scrub_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        asyncio.run(scrub("does-not-exist.heic"))
