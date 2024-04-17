import base64

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.config import settings as s


class Cipherer:
    """
    The class is a coder.
    Public methods:
        encrypt(data: str, password: str | None) - encrypts data
        decrypt(data: str, password: str | None) - decrypts data
    """

    def __init__(self) -> None:
        self._cipher = Fernet(
            base64.urlsafe_b64decode(s.KEY)
        )

    def _get_kdf(self, salt: str):
        # Есть идея/мысль на улучшение криптозащиты:
        # использовать новую (случайную) соль с каждым шифрованием
        # а саму соль сохранять в первых или последних байтах
        # результата шифрования
        return PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode('utf-8'),
            iterations=480000,
        )

    def _get_cipher(self, password: str | None = None) -> Fernet:
        """
        We'll encrypt everything. Either a password or our key.
        If no password is passed, it returns the shared key.
        """
        if password is not None:
            kdf = self._get_kdf(s.SALT)
            key = kdf.derive(password.encode('utf-8'))
            cipher = Fernet(base64.urlsafe_b64encode(key))
        else:
            cipher = self._cipher
        return cipher

    def encrypt(self,
                data: str,
                password: str | None = None
                ) -> str:
        """
        Securely encrypts the transmitted string. Either the transmitted
        password or the default encryption key will be used.
        """
        cipher = self._get_cipher(password=password)
        encrypted = cipher.encrypt(data.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')

    def decrypt(self,
                data: str,
                password: str | None = None
                ) -> tuple[str, bool]:
        """
        Decrypts data using a password
        or standard key if no password is available.
        """
        cipher = self._get_cipher(password=password)
        try:
            decrypted = cipher.decrypt(
                base64.urlsafe_b64decode(data)  # .encode('utf-8')
            )
            return decrypted.decode('utf-8'), True
        except InvalidToken:
            return "", False
