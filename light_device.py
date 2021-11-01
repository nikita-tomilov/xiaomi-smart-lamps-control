from yeelight import LightType, Bulb


class LightDevice:

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

    def turn_on(self):
        self.lamp.turn_on(light_type=self.light_type)

    def turn_off(self):
        self.lamp.turn_off(light_type=self.light_type)

    def toggle(self):
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
            self.lamp.set_rgb(self.r, self.g, self.b, light_type=self.light_type)

    def apply_white(self):
        if self.supports_white:
            self.lamp.set_color_temp(self.wb, light_type=self.light_type)
            self.lamp.set_brightness(self.brightness, light_type=self.light_type)

    def get_hex_rgb(self):
        return '%02x%02x%02x' % (self.r, self.g, self.b)

    def get_props(self):
        i = self.lamp.get_properties()
        return 1
