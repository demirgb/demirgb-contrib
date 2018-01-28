#!/usr/bin/env micropython

import machine
import time
import ustruct
import socket

LED_R_PIN = 13  # D7 on the D1 Mini
LED_G_PIN = 12  # D6 on the D1 Mini
LED_B_PIN = 14  # D5 on the D1 Mini
PWM_HZ = 240
LISTEN_ADDR = '0.0.0.0'
LISTEN_PORT = 26079


def bsd_checksum(input):
    checksum = 0
    for ch in input:
        checksum = (checksum >> 1) + ((checksum & 1) << 15)
        checksum += ch
        checksum &= 0xffff
    return checksum


def jtlvi_loads(input):
    input_len = len(input)
    output = []

    assert(input[0:2] == b'\xd4\x0e')
    assert(input_len >= 4)
    input_checksum = ustruct.unpack('!H', input[2:4])[0]
    input_zeroed = b'\xd4\x0e\x00\x00' + input[4:]
    calculated_checksum = bsd_checksum(input_zeroed)
    assert(calculated_checksum == input_checksum)

    pos = 4
    while input_len > pos:
        assert(input_len >= (pos + 4))
        t = ustruct.unpack('!H', input[pos:pos+2])[0]
        if t == 65535:
            break
        l = ustruct.unpack('!H', input[pos+2:pos+4])[0]
        assert(input_len >= (pos + 4 + l))
        v = input[pos+4:pos+4+l]
        output.append((t, v))
        pos += 4 + l

    return output


def process_msg(data, addr):
    tag_defs = {
        1: (LED_R, 'Red'),
        2: (LED_G, 'Green'),
        3: (LED_B, 'Blue'),
    }
    print('Packet received from {}'.format(addr))
    for (t, v) in jtlvi_loads(data):
        if t not in tag_defs:
            continue
        (led, desc) = tag_defs[t]
        numeric_val = ustruct.unpack('!H', v)[0]
        if numeric_val > 1023:
            continue
        print('Setting {} to {}'.format(desc, numeric_val))
        led.duty(numeric_val)
    print()


LED_R = machine.PWM(machine.Pin(LED_R_PIN), freq=PWM_HZ, duty=0)
LED_G = machine.PWM(machine.Pin(LED_G_PIN), freq=PWM_HZ, duty=0)
LED_B = machine.PWM(machine.Pin(LED_B_PIN), freq=PWM_HZ, duty=0)


def main():
    for led in (LED_R, LED_G, LED_B):
        led.duty(1023)
        time.sleep(1)
        led.duty(0)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_ADDR, LISTEN_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        try:
            process_msg(data, addr)
        except:
            continue
