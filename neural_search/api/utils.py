import hashlib


def sha256(text):
    # 텍스트를 바이트로 인코딩
    encoded_text = text.encode("utf-8")
    # SHA-256 해시 생성
    sha256_hash = hashlib.sha256(encoded_text).hexdigest()
    return sha256_hash
