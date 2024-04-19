import pytest
from src.secrets.cipherer import Cipherer


@pytest.fixture
def cipherer():
    return Cipherer()


# Тест 1: Шифрование и расшифровка без пароля
def test_encrypt_decrypt_no_password(cipherer):
    original_data = "Test data"
    encrypted_data = cipherer.encrypt(original_data)
    assert encrypted_data != original_data  # Убедимся, что данные зашифрованы

    decrypted_data, success = cipherer.decrypt(encrypted_data)
    assert success is True
    assert decrypted_data == original_data  # Убедимся, что данные успешно расшифрованы


# Тест 2: Шифрование и расшифровка с паролем
def test_encrypt_decrypt_with_password(cipherer):
    original_data = "Secret data"
    password = "securepassword123"

    encrypted_data = cipherer.encrypt(original_data, password)
    assert encrypted_data != original_data  # Данные зашифрованы

    # Попытка расшифровать без пароля
    decrypted_data, success = cipherer.decrypt(encrypted_data)
    assert success is False
    assert decrypted_data == ""

    # Попытка расшифровать с неправильным паролем
    wrong_password = "wrongpassword"
    decrypted_data, success = cipherer.decrypt(encrypted_data, wrong_password)
    assert success is False
    assert decrypted_data == ""

    # Расшифровка с правильным паролем
    decrypted_data, success = cipherer.decrypt(encrypted_data, password)
    assert success is True
    assert decrypted_data == original_data


@pytest.mark.parametrize(
    "data, password",
    [
        ("Data with special chars !@#$%^&*()_+-=", "simplepassword"),
        ("Текст на русском", "пароль"),
        ("数据和密码", "密码"),  # Китайские символы в данных и пароле
        ("🌟 Emoji 🌟", "🔑 EmojiKey 🔑"),  # Эмодзи в данных и пароле
        ("Normal text", "密码"),  # Обычный текст, пароль на китайском
        ("密码", "Normal password"),  # Китайский текст, обычный пароль
    ],
)
def test_encrypt_decrypt_unicode(cipherer, data, password):
    encrypted_data = cipherer.encrypt(data, password)
    assert encrypted_data != data  # Убедимся, что данные зашифрованы

    decrypted_data, success = cipherer.decrypt(encrypted_data, password)
    assert success is True
    assert decrypted_data == data  # Убедимся, что данные успешно расшифрованы

    # Проверка расшифровки с неправильным паролем
    wrong_password = password + "wrong"
    decrypted_data, success = cipherer.decrypt(encrypted_data, wrong_password)
    assert success is False
    assert decrypted_data == ""
