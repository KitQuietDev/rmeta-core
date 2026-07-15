from rmeta_core.utils.pii_scanner import scan_text_for_pii


def test_detects_email():
    assert "email" in scan_text_for_pii("reach me at jane@example.com")


def test_detects_ssn():
    assert "ssn" in scan_text_for_pii("SSN: 123-45-6789")


def test_detects_phone():
    assert "phone" in scan_text_for_pii("call 555-123-4567")


def test_detects_name():
    assert "name" in scan_text_for_pii("signed, Jane Smith")


def test_clean_text_flags_nothing():
    found = scan_text_for_pii("the quick brown fox jumps over the lazy dog")
    assert found == set()
