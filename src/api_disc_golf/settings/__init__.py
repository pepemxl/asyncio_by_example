"""
    This settings file permits us to centralize settings for each microservice and stage.
"""
import os
import socket
import sys


SOCKET_FQDN = socket.getfqdn()
IS_DEV = True if SOCKET_FQDN.lower().startswith("dev") > -1 else False
IS_CANARY = True if SOCKET_FQDN.lower().startswith("canary") > -1 else False
IS_CONTROL = True if SOCKET_FQDN.lower().startswith("control") > -1 else False
IS_LATEST = True if SOCKET_FQDN.lower().startswith("latest") > -1 else False
IS_PRODUCTION = True if SOCKET_FQDN.lower().startswith("production") > -1 else False

if __name__ == '__main__':
    print(SOCKET_FQDN)