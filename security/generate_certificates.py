import os
from datetime import datetime, timedelta
import ipaddress

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERT_DIR = os.path.join(BASE_DIR, "certificates")

os.makedirs(CERT_DIR, exist_ok=True)


def generate_ca():
    key = rsa.generate_private_key(65537, 2048)

    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "Secure CA"),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True
        )
        .sign(key, hashes.SHA256())
    )

    with open(os.path.join(CERT_DIR, "ca.key"), "wb") as f:
        f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        ))

    with open(os.path.join(CERT_DIR, "ca.crt"), "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    return key, cert


def generate_server_cert(ca_key, ca_cert):
    server_key = rsa.generate_private_key(65537, 2048)

    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
            ]),
            critical=False
        )
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True
        )
        .sign(ca_key, hashes.SHA256())
    )

    with open(os.path.join(CERT_DIR, "server.key"), "wb") as f:
        f.write(server_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        ))

    with open(os.path.join(CERT_DIR, "server.crt"), "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


if __name__ == "__main__":
    print("Generating certs...")
    ca_key, ca_cert = generate_ca()
    generate_server_cert(ca_key, ca_cert)
    print("DONE")