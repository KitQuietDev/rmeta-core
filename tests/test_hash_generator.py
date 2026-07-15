import hashlib

import pytest

from rmeta_core.postprocessors.hash_generator import generate_hash


def test_generate_hash_matches_manual_computation(dirty_txt):
    expected = hashlib.sha256(dirty_txt.read_bytes()).hexdigest()

    hash_filename = generate_hash(str(dirty_txt), algo="sha256")

    hash_path = dirty_txt.parent / hash_filename
    assert hash_path.exists()
    content = hash_path.read_text()
    assert expected in content
    assert dirty_txt.name in content


def test_generate_hash_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        generate_hash("does-not-exist.txt")


def test_generate_hash_unsupported_algo_raises(dirty_txt):
    with pytest.raises(ValueError):
        generate_hash(str(dirty_txt), algo="not-a-real-algo")
