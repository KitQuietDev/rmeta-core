from rmeta_core.handlers import get_handler_for_extension, handler_map

EXPECTED_EXTENSIONS = {"pdf", "docx", "xlsx", "jpg", "jpeg", "png", "heic", "txt", "csv"}


def test_all_expected_handlers_registered():
    missing = EXPECTED_EXTENSIONS - set(handler_map.keys())
    assert not missing, f"missing handlers for: {missing}"


def test_get_handler_for_extension_is_case_insensitive():
    assert get_handler_for_extension("PDF") is get_handler_for_extension("pdf")


def test_unknown_extension_returns_none():
    assert get_handler_for_extension("exe") is None


def test_pii_detect_flags():
    assert handler_map["pdf"]["pii_detect"] is True
    assert handler_map["docx"]["pii_detect"] is True
    assert handler_map["xlsx"]["pii_detect"] is True
    assert handler_map["jpg"]["pii_detect"] is False
    assert handler_map["heic"]["pii_detect"] is False
