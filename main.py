#!/usr/bin/env python3
import threading
import time

from flask import Flask, send_from_directory
from flask import render_template
from yeelight import LightType, flows

from light_device import LightDevice
from socket_device import SocketDevice

app = Flask(__name__, template_folder="./template/")

devices = {
    'bulb': LightDevice(identifier="bulb", name="Bulb", ip="192.168.0.111", supports_rgb=True, supports_white=True,
                        brightness=100, wb=5600),
    'desk_lamp': LightDevice(identifier="desk_lamp", name="Desk Lamp", ip="192.168.0.108", supports_rgb=False,
                             supports_white=True, brightness=100, wb=5600),
    'desk_lamp_bg': LightDevice(identifier="desk_lamp_bg", name="Desk Lamp (Background)", ip="192.168.0.108",
                                supports_rgb=True, supports_white=True, light_type=LightType.Ambient),
    'socket': SocketDevice(identifier="socket", name="Socket", ip="192.168.0.172",
                           token="827a5640037a78c26c2af4fd71d7aba5")
}

wb_swatches = [
    [2700, "#fddf83"],
    [3500, "#fcf4d6"],
    [4000, "#fffff7"],
    [5000, "#ffffff"],
    [5500, "#f2fdff"],
    [6500, "#e6f8ff"],
]

light_presets = [
    10, 25, 50, 75, 100
]

flow_presets = {
    'alarm': flows.alarm(),
    'candle_flicker': flows.candle_flicker(),
    'christmas': flows.christmas(),
    'date_night': flows.date_night(),
    'disco': flows.disco(),
    'happy_birthday': flows.happy_birthday(),
    'home': flows.home(),
    'lsd': flows.lsd(),
    'movie': flows.movie(),
    'night_mode': flows.night_mode(),
    'police': flows.police(),
    'police2': flows.police2(),
    'pulse': flows.pulse(255, 255, 255),
    'random_loop': flows.random_loop(),
    'rgb': flows.rgb(),
    'romance': flows.romance(),
    'slowdown': flows.slowdown(),
    'strobe': flows.strobe(),
    'strobe_color': flows.strobe_color(),
    'sunrise': flows.sunrise(),
    'sunset': flows.sunset(),
    'temp': flows.temp()
}


@app.route('/')
def http_main_entry():
    return render_template('index.html', devices=list(devices.values()), wb_swatches=wb_swatches,
                           light_presets=light_presets, flow_presets=list(flow_presets.keys()))


@app.route('/colour/<dev_id>/<r>/<g>/<b>')
def change_colour(dev_id, r, g, b):
    r = int(r)
    g = int(g)
    b = int(b)
    if dev_id in devices:
        device = devices[dev_id]
        device.r = r
        device.g = g
        device.b = b
        device.apply_rgb()
        print("changed", dev_id, "colour to", r, g, b)
        return "ok"
    else:
        return "no dev " + dev_id + "found"


@app.route('/switch/<dev_id>/<state>')
def switch(dev_id, state):
    if dev_id in devices:
        device = devices[dev_id]
        device.switch(state)
        print("switched", dev_id, "to state", state)
        return "ok"
    else:
        return "no dev " + dev_id + "found"


@app.route('/flow/<dev_id>/<flow_name>')
def flow(dev_id, flow_name):
    if dev_id in devices:
        if flow_name in flow_presets:
            device = devices[dev_id]
            flow_preset = flow_presets[flow_name]
            device.go_flow(flow_preset)
            print("switched", dev_id, "to flow", flow_name)
            return "ok"
    else:
        return "no dev " + dev_id + "found"


# noinspection DuplicatedCode
@app.route('/brightness/<dev_id>/<value>')
def change_brightness(dev_id, value):
    value = int(value)
    if dev_id in devices:
        device = devices[dev_id]
        device.brightness = value
        device.apply_white()
        print("switched", dev_id, "brightness to", value)
        return "ok"
    else:
        return "no dev " + dev_id + "found"


# noinspection DuplicatedCode
@app.route('/wb/<dev_id>/<value>')
def change_white_balance(dev_id, value):
    value = int(value)
    if dev_id in devices:
        device = devices[dev_id]
        device.wb = value
        device.apply_white()
        print("switched", dev_id, "brightness to", value)
        return "ok"
    else:
        return "no dev " + dev_id + "found"


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('template', path)


# noinspection PyBroadException
def device_info_updater():
    while True:
        for device in list(devices.values()):
            try:
                device.update()
            except Exception:
                print("error in device_info_updater over device ", device.identifier)
            time.sleep(2)


if __name__ == '__main__':
    devices['desk_lamp_bg'].lamp = devices['desk_lamp'].lamp
    updater_thread = threading.Thread(target=device_info_updater)
    updater_thread.daemon = True
    updater_thread.start()
    app.run(host='0.0.0.0', port=8139, threaded=True)
