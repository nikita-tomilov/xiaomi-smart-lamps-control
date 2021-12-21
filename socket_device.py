import threading

import miio


class SocketDevice:

    def __init__(self, identifier, name, ip, token):
        self.identifier = identifier
        self.name = name
        self.ip = ip
        self.token = token
        self.mode = "not known yet"
        self.plug = miio.ChuangmiPlug(ip=ip, token=token)
        self.lock = threading.Lock()
        self.props_cache = None

    def turn_on(self):
        with self.lock:
            self.plug.on()

    def turn_off(self):
        with self.lock:
            self.plug.off()

    def switch(self, state):
        if state == "on":
            self.turn_on()
        elif state == "off":
            self.turn_off()
        self.update()

    def update(self):
        with self.lock:
            self.props_cache = self.plug.status()
            self.mode = "on" if self.props_cache.is_on else "off"
            self.mode += "; load=" + str(self.props_cache.load_power)
            self.mode += "; temp=" + str(self.props_cache.temperature)
