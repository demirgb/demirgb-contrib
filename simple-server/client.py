#!/usr/bin/env python3

import jtlvi
import sys
import socket
import struct
import binascii
import os
import argparse


def parse_args(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog=os.path.basename(argv[0]),
    )

    parser.add_argument(
        'host', type=str, default=None,
        help='DemiRGB JTLVI host',
    )
    parser.add_argument(
        '--port', dest='port', type=int, default=26079,
        help='DemiRGB JTLVI port',
    )
    parser.add_argument(
        '--hex', dest='hex', type=str,
        help='hex code to send (e.g. #ff0080)',
    )
    parser.add_argument(
        '--raw', dest='raw', type=str,
        help='raw values to send for R,G,B, 0-1023 (e.g. 123,0,1023)',
    )
    parser.add_argument(
        '--password', dest='password', type=str,
        help='device password',
    )

    args = parser.parse_args(args=argv[1:])

    if ((not args.hex) and (not args.raw)) or (args.hex and args.raw):
        parser.error('Must specify --hex or --raw')

    return args


if __name__ == '__main__':
    args = parse_args()
    if args.hex:
        (R, G, B) = binascii.unhexlify(args.hex[1:])
        R = int(R / 255.0 * 1023.0)
        G = int(G / 255.0 * 1023.0)
        B = int(B / 255.0 * 1023.0)
    else:
        (R, G, B) = [int(i) for i in args.raw.split(',')]

    msg = {
        1: struct.pack('!H', R),
        2: struct.pack('!H', G),
        3: struct.pack('!H', B),
    }
    if args.password:
        msg[4] = args.password.encode('UTF-8')

    data = jtlvi.dumps(msg)
    print('Sending to {}:\n    {}\n    {}'.format(
        (args.host, args.port),
        msg,
        data,
    ))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (args.host, args.port))
