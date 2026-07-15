from rmeta_core.utils.cleanup import purge_uploads, check_uploads_dir


def test_check_uploads_dir_false_when_missing(tmp_path):
    assert check_uploads_dir(str(tmp_path / "does-not-exist")) is False


def test_check_uploads_dir_true_when_has_files(tmp_path):
    (tmp_path / "file.txt").write_text("hello")
    assert check_uploads_dir(str(tmp_path)) is True


def test_purge_uploads_removes_files(tmp_path):
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "b.txt").write_text("world")

    result = purge_uploads(str(tmp_path))

    assert result is True
    assert list(tmp_path.iterdir()) == []


def test_purge_uploads_false_when_already_clean(tmp_path):
    assert purge_uploads(str(tmp_path)) is False


def test_purge_uploads_false_when_missing(tmp_path):
    assert purge_uploads(str(tmp_path / "does-not-exist")) is False
