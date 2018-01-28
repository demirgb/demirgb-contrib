#!/usr/bin/env python3

import jtlvi
import sys
import socket
import struct
import binascii

SERVER_PORT = 26079
SERVER_ADDR = sys.argv[1]
c = sys.argv[2]
if c.startswith('#') and len(c) == 7:
    # Input is HTML color hex
    (R, G, B) = binascii.unhexlify(c[1:])
    R = int(R / 255.0 * 1023.0)
    G = int(G / 255.0 * 1023.0)
    B = int(B / 255.0 * 1023.0)
else:
    # Input is raw 0-1023 values for R/G/B
    R = int(sys.argv[2])
    G = int(sys.argv[3])
    B = int(sys.argv[4])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = {
    1: struct.pack('!H', R),
    2: struct.pack('!H', G),
    3: struct.pack('!H', B),
}
data = jtlvi.dumps(msg)
print('Sending to {}:\n    {}\n    {}'.format(
    (SERVER_ADDR, SERVER_PORT),
    msg,
    data,
))
sock.sendto(data, (SERVER_ADDR, SERVER_PORT))
