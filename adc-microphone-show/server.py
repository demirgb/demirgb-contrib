import time
import machine


LED_R_PIN = 13  # D7 on the D1 Mini
LED_G_PIN = 12  # D6 on the D1 Mini
LED_B_PIN = 14  # D5 on the D1 Mini
PWM_HZ = 240
SAMPLE_WINDOW = 50
EWMA_DECAY = 1.5
SPEED = 45

LED_R = machine.PWM(machine.Pin(LED_R_PIN), freq=PWM_HZ, duty=0)
LED_G = machine.PWM(machine.Pin(LED_G_PIN), freq=PWM_HZ, duty=0)
LED_B = machine.PWM(machine.Pin(LED_B_PIN), freq=PWM_HZ, duty=0)
adc = machine.ADC(0)
EWMA = -1


def get_peak_peak():
    start_ms = time.ticks_ms()
    signal_max = 0
    signal_min = 1023
    while (time.ticks_ms() - start_ms) < SAMPLE_WINDOW:
        sample = adc.read()
        if sample > 1023:
            sample = 1023
        if sample > signal_max:
            signal_max = sample
        if sample < signal_min:
            signal_min = sample
    return(signal_max - signal_min)


def hsv_to_rgb(h, s, v):
    # In: 0.0 to 1.0 ranges
    # Out: 0.0 to 1.0 ranges
    if s == 0.0:
        return (v, v, v)
    i = int(h*6.)  # assume int() truncates
    f = (h*6.)-i
    p, q, t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f))
    i %= 6
    if i == 0:
        return (v, t, p)
    elif i == 1:
        return (q, v, p)
    elif i == 2:
        return (p, v, t)
    elif i == 3:
        return (p, q, v)
    elif i == 4:
        return (t, p, v)
    elif i == 5:
        return (v, p, q)


def reset():
    LED_R.duty(0)
    LED_G.duty(0)
    LED_B.duty(0)


def variant1():
    global EWMA
    for i in range(SPEED):
        v = get_peak_peak()
        if EWMA == -1:
            EWMA = v * EWMA_DECAY
        else:
            EWMA += (v - (EWMA / EWMA_DECAY))
        r, g, b = hsv_to_rgb(i / SPEED, 1.0, EWMA / EWMA_DECAY / 512.0)
        LED_R.duty(int(r * 1023))
        LED_G.duty(int(g * 1023))
        LED_B.duty(int(b * 1023))


def variant2():
    global EWMA
    for i in range(SPEED * 2):
        v = get_peak_peak()
        if EWMA == -1:
            EWMA = v * EWMA_DECAY
        else:
            EWMA += (v - (EWMA / EWMA_DECAY))
        r, g, b = hsv_to_rgb(EWMA / EWMA_DECAY / 512.0, 1.0, abs(i - SPEED) / SPEED)
        LED_R.duty(int(r * 1023))
        LED_G.duty(int(g * 1023))
        LED_B.duty(int(b * 1023))


def loop():
    while True:
        for i in (variant1,):
            i()


def main():
    try:
        loop()
    except KeyboardInterrupt:
        reset()


if __name__ == '__main__':
    main()
