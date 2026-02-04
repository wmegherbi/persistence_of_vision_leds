import threading
import time

from flask import Flask, render_template, request, jsonify
import pigpio

GPIO_PWM = 18
GPIO_HALL = 17
GPIO_REV_PULSE = 27

MAX_EDGES = 20
REV_PULSE_US = 100
MAX_PULSES = 200
PULSE_WINDOW_S = 5.0

app = Flask(__name__)

lock = threading.Lock()
hall_count = 0
edge_times = []
pulse_times = []
magnets_per_rev = 4
current_pwm = 1000

pi = pigpio.pi()
if not pi.connected:
    raise Exception("pigpiod n'est pas lance : sudo pigpiod")

pi.set_mode(GPIO_HALL, pigpio.INPUT)
pi.set_pull_up_down(GPIO_HALL, pigpio.PUD_UP)

pi.set_mode(GPIO_REV_PULSE, pigpio.OUTPUT)
pi.write(GPIO_REV_PULSE, 0)


def hall_callback(gpio, level, tick):
    global hall_count, edge_times, pulse_times

    now = time.time()
    with lock:
        if level == 1:
            hall_count += 1
            edge_times.append(now)
            if len(edge_times) > MAX_EDGES:
                edge_times.pop(0)

            if magnets_per_rev > 0 and hall_count % magnets_per_rev == 0:
                pi.gpio_trigger(GPIO_REV_PULSE, REV_PULSE_US, 1)
                pulse_times.append(now)
                if len(pulse_times) > MAX_PULSES:
                    pulse_times.pop(0)


cb = pi.callback(GPIO_HALL, pigpio.EITHER_EDGE, hall_callback)


@app.route("/")
def index():
    with lock:
        return render_template(
            "index.html",
            value=current_pwm,
            hall_count=hall_count,
            magnets_per_rev=magnets_per_rev,
        )


@app.route("/set_live", methods=["POST"])
def set_live():
    global current_pwm
    pwm = int(request.form["pwm"])
    current_pwm = pwm
    pi.set_servo_pulsewidth(GPIO_PWM, pwm)
    return ""


@app.route("/stop", methods=["POST"])
def stop():
    global current_pwm
    current_pwm = 1000
    pi.set_servo_pulsewidth(GPIO_PWM, 1000)
    with lock:
        return render_template(
            "index.html",
            value=current_pwm,
            hall_count=hall_count,
            magnets_per_rev=magnets_per_rev,
        )


@app.route("/api/hall")
def hall_api():
    with lock:
        rpm = 0
        if magnets_per_rev > 0 and len(edge_times) >= 2:
            period = (edge_times[-1] - edge_times[0]) / (len(edge_times) - 1)
            if period > 0:
                rpm = round(60 / (period * magnets_per_rev), 1)

        return jsonify({
            "count": hall_count,
            "magnets_per_rev": magnets_per_rev,
            "rpm": rpm,
        })


@app.route("/api/pulse")
def pulse_api():
    with lock:
        now = time.time()
        recent = [t for t in pulse_times if now - t <= PULSE_WINDOW_S]
        pulse_times[:] = recent
        return jsonify([{"t": t} for t in recent])


def cleanup():
    cb.cancel()
    pi.stop()


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        cleanup()
