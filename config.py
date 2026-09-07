import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HOST = "localhost"
PORT = 8443

CERT_DIR = os.path.join(BASE_DIR, "certificates")

CA_FILE = os.path.join(CERT_DIR, "ca.crt")
SERVER_CERT = os.path.join(CERT_DIR, "server.crt")
SERVER_KEY = os.path.join(CERT_DIR, "server.key")

LOG_FILE = os.path.join(BASE_DIR, "logs", "tls.log")