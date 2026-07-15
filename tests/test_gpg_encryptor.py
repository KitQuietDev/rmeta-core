import shutil
import subprocess

import pytest

from rmeta_core.postprocessors.gpg_encryptor import encrypt_with_gpg

pytestmark = pytest.mark.skipif(shutil.which("gpg") is None, reason="gpg binary not available")


@pytest.fixture
def gpg_public_key(tmp_path):
    gpg_home = tmp_path / "gpg_home"
    gpg_home.mkdir(mode=0o700)

    subprocess.run(
        [
            "gpg", "--homedir", str(gpg_home), "--batch", "--passphrase", "",
            "--quick-generate-key", "Test User <test@example.com>", "default", "default", "never",
        ],
        check=True, capture_output=True,
    )

    key_path = tmp_path / "pubkey.asc"
    result = subprocess.run(
        ["gpg", "--homedir", str(gpg_home), "--armor", "--export", "test@example.com"],
        check=True, capture_output=True,
    )
    key_path.write_bytes(result.stdout)
    return key_path


def test_encrypt_produces_valid_gpg_file(dirty_txt, gpg_public_key):
    result_name = encrypt_with_gpg(str(dirty_txt), str(gpg_public_key))

    encrypted_path = dirty_txt.parent / result_name
    assert encrypted_path.exists()
    assert encrypted_path.stat().st_size > 0
    # GPG binary/ASCII output starts with a recognizable packet header
    assert encrypted_path.read_bytes()[:1] in (b"\x84", b"\x85", b"-")


def test_encrypt_missing_file_raises(gpg_public_key):
    with pytest.raises(FileNotFoundError):
        encrypt_with_gpg("does-not-exist.txt", str(gpg_public_key))


def test_encrypt_missing_key_raises(dirty_txt, tmp_path):
    with pytest.raises(FileNotFoundError):
        encrypt_with_gpg(str(dirty_txt), str(tmp_path / "no-such-key.asc"))
