from rmeta_core.utils.chunking import audit_files, chunk_files_by_size


def test_audit_files_reports_missing(tmp_path):
    missing = str(tmp_path / "nope.txt")
    supported, too_large, skipped = audit_files([missing], min_memory_mb=512)
    assert supported == []
    assert skipped == [(missing, "Missing")]


def test_audit_files_reports_unsupported_extension(tmp_path):
    bogus = tmp_path / "file.exe"
    bogus.write_text("x")
    supported, too_large, skipped = audit_files([str(bogus)], min_memory_mb=512)
    assert supported == []
    assert skipped == [(str(bogus), "Unsupported")]


def test_audit_files_reports_supported(dirty_txt):
    supported, too_large, skipped = audit_files([str(dirty_txt)], min_memory_mb=512)
    assert supported == [str(dirty_txt)]
    assert too_large == []
    assert skipped == []


def test_audit_files_reports_too_large(tmp_path):
    big = tmp_path / "big.txt"
    big.write_bytes(b"x" * 2048)  # 2KB
    supported, too_large, skipped = audit_files([str(big)], min_memory_mb=0.001)
    assert supported == []
    assert too_large[0][0] == str(big)


def test_chunk_files_by_size_groups_by_limit(tmp_path):
    files = []
    for i in range(3):
        f = tmp_path / f"file{i}.txt"
        f.write_bytes(b"x" * (1024 * 1024))  # 1MB each
        files.append(str(f))

    chunks = chunk_files_by_size(files, chunk_mb=2)

    assert sum(len(c) for c in chunks) == 3
    assert all(len(c) <= 2 for c in chunks)
