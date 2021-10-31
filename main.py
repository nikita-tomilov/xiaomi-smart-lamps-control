#!/usr/bin/env python3

from flask import Flask, redirect, send_from_directory
from flask import render_template
from yeelight import Bulb, LightType, discover_bulbs

app = Flask(__name__, template_folder="./template/")
bulb = Bulb("192.168.0.111", auto_on=True)
bulb_brightness = 100
bulb_color_temp = 5600
desk_lamp = Bulb("192.168.0.108", auto_on=True)
desk_lamp_brightness = 100
desk_lamp_color_temp = 5600
desk_lamp_background_brightness = 100
desk_lamp_background_color_temp = 5600


def bulb_toggle(blb, state, light_type=LightType.Main):
    if state == "on":
        blb.turn_on(light_type)
    elif state == "off":
        blb.turn_off(light_type)
    if state == "toggle":
        blb.toggle(light_type)


def bulb_update_plain_params(blb, brightness, color_temp, light_type=LightType.Main):
    blb.set_color_temp(color_temp, light_type)
    blb.set_brightness(brightness, light_type)


@app.route('/')
def http_main_entry():
    return render_template('index.html') # , mode=current_mode)


@app.route('/colour/<dev>/<r>/<g>/<b>')
def change_colour(dev, r, g, b):
    r = int(r)
    g = int(g)
    b = int(b)
    if dev == "bulb":
        bulb.set_rgb(r, g, b)
    elif dev == "desk_lamp_background":
        desk_lamp.set_rgb(r, g, b, light_type=LightType.Ambient)
    print("changed", dev, "colour to", r, g, b)
    return "ok"


@app.route('/switch/<dev>/<state>')
def switch(dev, state):
    if dev == "bulb":
        bulb_toggle(bulb, state)
    elif dev == "desk_lamp":
        bulb_toggle(desk_lamp, state)
    elif dev == "desk_lamp_background":
        bulb_toggle(desk_lamp, state, light_type=LightType.Ambient)
    print("switched", dev, "to", state)
    return "ok"


@app.route('/brightness/<dev>/<value>')
def change_brightness(dev, value):
    value = int(value)
    global bulb_brightness, bulb_color_temp, desk_lamp_brightness, desk_lamp_color_temp
    if dev == "bulb":
        global bulb_brightness, bulb_color_temp
        bulb_brightness = value
        bulb_update_plain_params(bulb, bulb_brightness, bulb_color_temp)
    elif dev == "desk_lamp":
        global desk_lamp_brightness, desk_lamp_color_temp
        desk_lamp_brightness = value
        bulb_update_plain_params(desk_lamp, desk_lamp_brightness, desk_lamp_color_temp)
    elif dev == "desk_lamp_background":
        global desk_lamp_background_brightness, desk_lamp_background_color_temp
        desk_lamp_background_brightness = value
        bulb_update_plain_params(desk_lamp, desk_lamp_background_brightness, desk_lamp_background_color_temp, light_type=LightType.Ambient)
    print("changed", dev, "brightness to", value)
    return "ok"


@app.route('/ct/<dev>/<value>')
def change_colour_temp(dev, value):
    value = int(value)
    if dev == "bulb":
        global bulb_brightness, bulb_color_temp
        bulb_color_temp = value
        bulb_update_plain_params(bulb, bulb_brightness, bulb_color_temp)
    elif dev == "desk_lamp":
        global desk_lamp_brightness, desk_lamp_color_temp
        desk_lamp_color_temp = value
        bulb_update_plain_params(desk_lamp, desk_lamp_brightness, desk_lamp_color_temp)
    elif dev == "desk_lamp_background":
        global desk_lamp_background_brightness, desk_lamp_background_color_temp
        desk_lamp_background_color_temp = value
        bulb_update_plain_params(desk_lamp, desk_lamp_background_brightness, desk_lamp_background_color_temp, light_type=LightType.Ambient)
    print("changed", dev, "colour temp to", value)
    return "ok"


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('template', path)


if __name__ == '__main__':
    #i = discover_bulbs()
    app.run(host='0.0.0.0', port=8139, threaded=True)