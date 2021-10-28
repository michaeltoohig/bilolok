from libthumbor import CryptoURL

from app.core.config import settings

img_crypto_url = CryptoURL(key=settings.THUMBOR_SECURITY_KEY)
