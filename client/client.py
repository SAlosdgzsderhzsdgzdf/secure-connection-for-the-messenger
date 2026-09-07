import socket
import ssl

from config import HOST, PORT
from security.handshake_logger import log_event


def main():
    # TLS без проверки сертификата 
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    sock = socket.create_connection((HOST, PORT))
    tls = context.wrap_socket(sock, server_hostname=HOST)

    print("Connected to secure server")
    log_event("CLIENT CONNECTED")

    try:
        while True:
            msg = input("Введите сообщение (or 'exit'): ")

            if msg.lower() == "exit":
                break

            tls.send(msg.encode())

            response = tls.recv(1024).decode()
            print("Server:", response)

            log_event(f"SENT: {msg} | RECEIVED: {response}")

    except Exception as e:
        log_event(f"CLIENT ERROR: {e}")

    finally:
        tls.close()
        log_event("CLIENT DISCONNECTED")


if __name__ == "__main__":
    main()