from homie.device import HomieDevice
from homie import __version__
from mqtt_as import MQTTClient
from homie.constants import (
    DEVICE_STATE,
    QOS,
    STATE_INIT,
    MAIN_DELAY
)
from machine import unique_id
from ubinascii import hexlify
from uasyncio import sleep_ms
from gc import collect


class MyHomieDevice(HomieDevice):

    def __init__(self, settings, ssid, password, mqttServer, mqttUser, mqttPassword):
        self.debug = getattr(settings, "DEBUG", False)

        self._state = STATE_INIT
        self._version = __version__
        self._fw_name = "Microhomie"
        self._extensions = getattr(settings, "EXTENSIONS", [])
        self._bc_enabled = getattr(settings, "BROADCAST", False)
        self._wifi = getattr(settings, "WIFI_CREDENTIALS", False)

        self.first_start = True
        self.stats_interval = getattr(settings, "DEVICE_STATS_INTERVAL", 60)
        self.device_name = getattr(settings, "DEVICE_NAME", "")
        self.callback_topics = {}

        # Registered homie nodes
        self.nodes = []

        # Generate unique id if settings has no DEVICE_ID
        self.device_id = getattr(settings, "DEVICE_ID", hexlify(unique_id()).decode())

        # Base topic
        self.btopic = getattr(settings, "MQTT_BASE_TOPIC", "homie")
        # Device base topic
        self.dtopic = "{}/{}".format(self.btopic, self.device_id)

        # mqtt_as client
        self.mqtt = MQTTClient(
            client_id=self.device_id,
            server=mqttServer,
            port=getattr(settings, "MQTT_PORT", 1883),
            user=mqttUser,
            password=mqttPassword,
            keepalive=getattr(settings, "MQTT_KEEPALIVE", 30),
            ping_interval=getattr(settings, "MQTT_PING_INTERVAL", 0),
            ssl=getattr(settings, "MQTT_SSL", False),
            ssl_params=getattr(settings, "MQTT_SSL_PARAMS", {}),
            response_time=getattr(settings, "MQTT_RESPONSE_TIME", 10),
            clean_init=getattr(settings, "MQTT_CLEAN_INIT", True),
            clean=getattr(settings, "MQTT_CLEAN", True),
            max_repubs=getattr(settings, "MQTT_MAX_REPUBS", 4),
            will=("{}/{}".format(self.dtopic, DEVICE_STATE), "lost", True, QOS),
            subs_cb=self.subs_cb,
            wifi_coro=None,
            connect_coro=self.connection_handler,
            ssid=ssid,
            wifi_pw=password,
        )

    async def run(self):
        while True:
            try:
                if self._wifi:
                    await self.setup_wifi()
                await self.mqtt.connect()
                while True:
                    collect()
                    print(".", end='')
                    await sleep_ms(MAIN_DELAY)
            except OSError:
                print("ERROR: can not connect to MQTT")
                await sleep_ms(5000)