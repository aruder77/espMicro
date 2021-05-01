from log_node import LogNode
from homie.device import HomieDevice
from homie import __version__
from mqtt_as import MQTTClient
from homie.constants import (
    DEVICE_STATE,
    QOS,
    STATE_INIT
)
from machine import unique_id
from ubinascii import hexlify
from uasyncio import sleep_ms
from gc import collect
from micropython import const
from utime import ticks_ms, ticks_diff, ticks_add

MAIN_DELAY = const(10)
LOOP_TIME = MAIN_DELAY * 10

class EspMicroDevice(HomieDevice):

    def __init__(self, settings, ssid, password, mqttServer, mqttUser, mqttPassword):
        super().__init__(settings)

        # Registered homie nodes
        self.logNode = LogNode(self) 
        self.add_node(self.logNode)

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
        counter = 0
        self.timer = ticks_ms()

        while True:
            try:
                if self._wifi:
                    await self.setup_wifi()
                await self.mqtt.connect()

                while True:
                    currentTime = ticks_ms()
                    await self.loop()

                    if (ticks_diff(currentTime, self.timer) > 0):
                        await self.every100Milliseconds()
                        for node in self.nodes:
                            await node.every100Milliseconds()

                        if (counter % 10 == 0):
                            collect()
                            await self.everySecond()
                            for node in self.nodes:
                                await node.everySecond()

                        if (counter % 100 == 0):
                            await self.every10Seconds()
                            for node in self.nodes:
                                await node.every10Seconds()

                        if (counter % 600 == 0):
                            await self.everyMinute()
                            for node in self.nodes:
                                await node.everyMinute()

                        if (counter % 36000 == 0):
                            await self.everyHour()
                            for node in self.nodes:
                                await node.everyHour()

                        if (counter % 864000 == 0):
                            await self.everyDay()
                            for node in self.nodes:
                                await node.everyDay()
                        
                        counter = counter + 1
                        if (counter > 864000):
                            counter = 0

                        self.timer = ticks_add(self.timer, LOOP_TIME)

            except OSError:
                print("ERROR: can not connect to MQTT")
                await sleep_ms(5000)


    async def loop(self):
        pass

    async def every100Milliseconds(self):
        pass

    async def everySecond(self):
        pass

    async def every10Seconds(self):
        pass

    async def everyMinute(self):
        pass

    async def everyHour(self):
        pass

    async def everyDay(self):
        pass

    def getLogger(self, name="root"):
        return self.logNode.getLogger(name)

        

