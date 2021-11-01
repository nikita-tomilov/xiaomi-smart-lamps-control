import threading

from yeelight import LightType, Bulb


def get_rgb_from_int(intstr):
    hexstr = "%06x" % intstr
    hexr = hexstr[0] + hexstr[1]
    hexg = hexstr[2] + hexstr[3]
    hexb = hexstr[4] + hexstr[5]
    r = int(hexr, 16)
    g = int(hexg, 16)
    b = int(hexb, 16)
    return r, g, b


def get_mode_str_from_int(intmode):
    if intmode == 1:
        return "rgb"
    elif intmode == 2:
        return "white"
    else:
        return "unknown, code " + str(intmode)


class LightDevice:
    props_cache = {}

    def __init__(self, identifier, name, ip, supports_rgb=False, r=0, g=255, b=0, supports_white=False, brightness=0,
                 wb=0,
                 light_type=LightType.Main):
        self.identifier = identifier
        self.name = name
        self.ip = ip
        self.supports_rgb = supports_rgb
        self.r = r
        self.g = g
        self.b = b
        self.supports_white = supports_white
        self.brightness = brightness
        self.wb = wb
        self.light_type = light_type
        self.lamp = Bulb(ip, auto_on=True)
        self.mode = "not known yet"
        self.lock = threading.Lock()

    def turn_on(self):
        with self.lock:
            self.lamp.turn_on(light_type=self.light_type)

    def turn_off(self):
        with self.lock:
            self.lamp.turn_off(light_type=self.light_type)

    def toggle(self):
        with self.lock:
            self.lamp.toggle(light_type=self.light_type)

    def switch(self, state):
        if state == "on":
            self.turn_on()
        elif state == "off":
            self.turn_off()
        if state == "toggle":
            self.toggle()

    def apply_rgb(self):
        if self.supports_rgb:
            with self.lock:
                self.lamp.set_rgb(self.r, self.g, self.b, light_type=self.light_type)

    def apply_white(self):
        if self.supports_white:
            with self.lock:
                self.lamp.set_color_temp(self.wb, light_type=self.light_type)
                self.lamp.set_brightness(self.brightness, light_type=self.light_type)

    def get_hex_rgb(self):
        return '%02x%02x%02x' % (self.r, self.g, self.b)

    def update(self):
        with self.lock:
            if self.light_type == LightType.Main:
                props = self.lamp.get_properties()
                LightDevice.props_cache[self.ip] = props
                # print("Props for ", self.identifier)
                self.mode = get_mode_str_from_int(int(props['color_mode']))
                # for k, v in props.items():
                #     print("  ", k, v)
                self.brightness = int(props['bright'])
                self.wb = int(props['ct'])
                r, g, b = get_rgb_from_int(int(props['rgb']))
                self.r = r
                self.g = g
                self.b = b
            else:
                props = LightDevice.props_cache[self.ip]
                # print("Props for ", self.identifier, "were assumed from cached props")
                self.brightness = int(props['bg_bright'])
                self.wb = int(props['bg_ct'])
                r, g, b = get_rgb_from_int(int(props['bg_rgb']))
                self.r = r
                self.g = g
                self.b = b
                self.mode = "n/a"
