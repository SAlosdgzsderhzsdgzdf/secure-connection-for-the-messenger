import ssl
from config import CA_FILE, SERVER_CERT, SERVER_KEY


def create_server_context():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    context.load_cert_chain(
        certfile=SERVER_CERT,
        keyfile=SERVER_KEY
    )

    return context


def create_client_context():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    context.load_verify_locations(cafile=CA_FILE)
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    return context