import cryptography
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

key = rsa.generate_private_key(
	public_exponent=65537,
	key_size=2048,
)
with open("C:/Users/tjime/Downloads/4/informatca/PWS/keys/key.pem", "wb") as f:
	f.write(key.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.TraditionalOpenSSL,
		encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
	))

crs = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
	x509.NameAttribute(NameOID.USER_ID, u"203975"),
	x509.NameAttribute(NameOID.COMMON_NAME, u"nuovo.itslearing.com"),
	x509.NameAttribute(NameOID.SURNAME, u"ten Berge"),
])).add_extension(
	x509.SubjectAlternativeName([
		x509.DNSName(u"nuovo.itslearing.com"),
		x509.DNSName(u"www.nuovo.itslearing.com"),
		x509.DNSName(u"subdomain.nuovo.itslearing.com"),
	]),
	critical=False,
).sign(key, hashes.SHA256())
with open("C:/Users/tjime/Downloads/4/informatca/PWS/keys/crs.pem", "wb") as f:
	f.write(crs.public_bytes(serialization.Encoding.PEM))
