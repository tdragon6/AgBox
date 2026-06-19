from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta, timezone
from pathlib import Path


def generate_cert(
    key_path: Path=Path(__file__).parent.parent / 'key.pem',
    cert_path: Path=Path(__file__).parent.parent / 'cert.pem'
) -> tuple[bool, str, None]:
    '''
    生成 https 证书
    '''
    if key_path.exists() and cert_path.exists():
        return True, 'success', None

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, 'AgBox'),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=36500))
        .sign(key, hashes.SHA256())
    )

    with key_path.open('wb') as f:
        f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
    
    with cert_path.open('wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    return True, 'success', None