from lib.homie.device import HomieDevice
from mqtt_as import MQTTClient
from homie.constants import (
    DEVICE_STATE,
    QOS
)


class MyHomieDevice(HomieDevice):

    def __init__(self, settings, ssid, password, mqttServer, mqttUser, mqttPassword):
        super().__init__(settings)

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
    