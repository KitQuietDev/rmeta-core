import asyncio

import pypdf
import pytest

from rmeta_core.handlers.pdf_handler import scrub, get_additional_messages


def test_scrub_removes_metadata(dirty_pdf):
    before = pypdf.PdfReader(str(dirty_pdf)).metadata
    assert before.get("/Author") == "MetaMaker"

    asyncio.run(scrub(str(dirty_pdf)))

    after = pypdf.PdfReader(str(dirty_pdf)).metadata
    assert not after or after.get("/Author") is None
    assert after.get("/Title") is None


def test_get_additional_messages_reports_scrub(dirty_pdf):
    asyncio.run(scrub(str(dirty_pdf)))
    messages = asyncio.run(get_additional_messages(str(dirty_pdf)))
    assert any("Metadata stripped" in m for m in messages)


def test_scrub_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        asyncio.run(scrub("does-not-exist.pdf"))
