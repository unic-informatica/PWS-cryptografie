import cryptography
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat import backends
from cryptography.hazmat.backends import default_backend
import base64

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b"password")
)
pem.splitlines()[0]

public_key = private_key.public_key()
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
pem.splitlines()[0]

message=b"testmessage"
message_bytes = bytes(message, encoding='utf8') if not isinstance(message, bytes) else message
text=public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        label=None,
        algorithm=hashes.SHA1
    )
)
text=str(base64.b64encode(text), encoding='utf-8')

public_key_pem_loaded = (bytes(
    public_key.pem_export,
    encoding='utf8'
) if not isinstance(public_key.pem_export, bytes) else public_key.pem_export)
public_key_pem_loaded = load_pem.public_key(
    data=public_key.pem_export,
    backend=default_backend()
)

data_to_sign = bytes(message, encoding='utf8') if not isinstance(
    message, 
    bytes
) else message
signer=private_key.signer(
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
signer.update(data_to_sign)
signature=str(
    base64.b64encode(signer.finalize()),
    encoding='utf8'
)
data=(text,signature)
text_decode=base64.b64decode(text) if not isinstance(text,bytes) else text
plain_text=private_key.decrypt(
    text_decode,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None
    )
)
plain_text=str(plain_text,encoding='utf8')
def check_sign():
    try:
        plain_text_bytes=bytes(
            plain_text,
            encoding='utf8',
        ) if not isinstance(plain_text,bytes) else plain_text
        signature=base64.b64decode(
            signature,
        ) if not isinstance(signature,bytes) else signature
        verifier=public_key.verifier(
            signature,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        verifier.update(plain_text_bytes),
        verifier.verify(),
        return True
    except InvalidSignature:
        return False