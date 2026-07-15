import asyncio

import pytest

from rmeta_core.handlers.text_csv_handler import scrub, get_additional_messages


def test_scrub_preserves_content(dirty_txt):
    original = dirty_txt.read_text(encoding="utf-8")
    asyncio.run(scrub(str(dirty_txt)))
    assert dirty_txt.read_text(encoding="utf-8") == original


def test_scrub_csv_preserves_content(dirty_csv):
    original = dirty_csv.read_text(encoding="utf-8")
    asyncio.run(scrub(str(dirty_csv)))
    assert dirty_csv.read_text(encoding="utf-8") == original


def test_get_additional_messages_flags_pii(dirty_txt):
    asyncio.run(scrub(str(dirty_txt)))
    messages = asyncio.run(get_additional_messages(str(dirty_txt)))
    assert any("PII detected" in m for m in messages)


def test_scrub_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        asyncio.run(scrub("does-not-exist.txt"))
