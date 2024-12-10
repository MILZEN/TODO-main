# Unit test: Util

from app import gen_hash, check_hash


def test_gen_hash_creates_hash():
    password = "my_secure_password"
    hashed_password = gen_hash(password)
    assert hashed_password != password  # El hash debe ser diferente al texto plano
    assert len(hashed_password) > 0  # El hash no debe estar vacío


def test_check_hash_valid():
    password = "my_secure_password"
    hashed_password = gen_hash(password)
    assert check_hash(password, hashed_password) is True  # Comparison must be valid


def test_check_hash_invalid():
    password = "my_secure_password"
    hashed_password = gen_hash(password)
    # Must fail with incorrect password
    assert check_hash("wrong_password", hashed_password) is False
