from libthumbor import CryptoURL

from core.config import settings

img_crypto_url = CryptoURL(key=settings.THUMBOR_SECURITY_KEY)
