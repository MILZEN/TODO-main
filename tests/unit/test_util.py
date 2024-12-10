# Unit test: Util

from app import gen_hash, check_hash


def test_gen_hash_creates_hash():
    password = "my_secure_password"
    hashed_password = gen_hash(password)
    assert hashed_password != password  # Hash must be different to plaintext
    assert len(hashed_password) > 0  # Hash must not be empty


def test_check_hash_valid():
    password = "my_secure_password"
    hashed_password = gen_hash(password)
    assert check_hash(password, hashed_password) is True  # Comparison must be valid


def test_check_hash_invalid():
    password = "my_secure_password"
    hashed_password = gen_hash(password)
    # Must fail with incorrect password
    assert check_hash("wrong_password", hashed_password) is False
