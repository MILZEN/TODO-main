# Prueba de Auth

from app import gen_hash, check_hash


def test_gen_hash():
    password = "test_password"
    hashed = gen_hash(password)
    assert hashed != password


def test_check_hash():
    password = "test_password"
    hashed = gen_hash(password)
    assert check_hash(password, hashed) is True
