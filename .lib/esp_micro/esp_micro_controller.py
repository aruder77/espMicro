import socket
import struct
import time

import settings
import network

from machine import Pin
import machine
from sys import platform

from esp_micro import singletons
from esp_micro.display_controller import DisplayController
from esp_micro.wifimgr import get_connection, do_connect
from homie.device import HomieDevice
from homie.network import get_local_ip
from homie.node import HomieNode
from homie.property import HomieProperty
from homie.constants import STRING
from primitives.pushbutton import Pushbutton
from esp_micro.logutil import get_logger
from esp_micro.ota_initializer import OtaInitializer, connectToWifi
from esp_micro.config_loader import read_profiles
from esp_micro.config_loader import read_mqtt
from esp_micro.config_loader import configured
from esp_micro.micro_controller_config import MicrocontrollerConfig, RP2PicoConfig, Esp32NodeMcuConfig, Esp32WroverKitConfig, \
    ArduinoNanoConnectConfig


class EspMicroController:

    def __init__(self):

        # setup logger
        self.logger = get_logger()

        singletons.microcontrollerConfig = self.create_microcontroller_config()
        singletons.displayController = self.create_display_controller()

        # setup boot button for config mode
        self.logger.info("setting up push button...")
        self.btn = Pushbutton(Pin(singletons.microcontrollerConfig.getButtonPin(), Pin.IN, Pin.PULL_UP))
        self.btn.long_func(self.enter_config_mode)

        self.logger.info("checking for connected")
        # read saved wifi and mqtt data
        if not configured():
            self.logger.info("not configured, entering configuration mode")
            get_connection()

        profiles = read_profiles()
        settings.WIFI_SSID = list(profiles.keys())[0]
        settings.WIFI_PASSWORD = profiles[settings.WIFI_SSID]
        connected = do_connect(settings.WIFI_SSID, settings.WIFI_PASSWORD)
        singletons.displayController.setWlanConnected(connected is not False)

        # read mqtt data
        (settings.MQTT_BROKER, settings.MQTT_USERNAME, settings.MQTT_PASSWORD, githubRepo, autoUpdate,
         unstableVersions) = read_mqtt()
        self.logger.info("mqtt settings: {} {} {} Tls:{}".format(settings.MQTT_BROKER, settings.MQTT_USERNAME, settings.MQTT_PASSWORD, settings.MQTT_SSL))
        self.otaInitializer = OtaInitializer(autoUpdate, unstableVersions)
        singletons.displayController.setAutoUpdate(autoUpdate)
        singletons.displayController.setIPAddress(get_local_ip().decode("utf-8"))

        if (connected is not False):
            self.otaInitializer.update()

        settings.DEVICE_ID = self.get_device_id()
        settings.DEVICE_NAME = self.get_device_name()

        # Homie device setup
        self.homie = self.create_homie_device(settings)

    def create_homie_device(self, settings) -> HomieDevice:
        print('You must override this method and return an EspMicroDevice subclass!')

    def get_device_name(self):
        print('You must override this method and return a device name!')

    def get_device_id(self):
        print('You must override this method and return a device ID!')

    def create_display_controller(self) -> DisplayController:
        return DisplayController()

    def create_microcontroller_config(self) -> MicrocontrollerConfig:
        if platform == "esp32":
            if settings.BOARD == "NodeMCU":
                self.logger.info('Using Esp32 NodeMCU setup.')
                return Esp32NodeMcuConfig()
            else:
                self.logger.info('Using Esp32WroverKit setup.')
                return Esp32WroverKitConfig()
        else:
            if settings.BOARD == "ARDUINO_NANO_RP2040_CONNECT":
                self.logger.info('Using Arduino Nano RP2040 Connect setup.')
                return ArduinoNanoConnectConfig()
            else:
                self.logger.info('Using Raspberry Pi Pico W setup.')
                return RP2PicoConfig()

    def create_esp_micro_node(self) -> HomieNode:
        node = HomieNode(id="espMicro", name="EspMicro", type="Controller", )

        update_property = HomieProperty(
            id="updateFirmware",
            name="Update firmware",
            settable=True,
            datatype=STRING,
            on_message=self.update_firmware
        )

        # Add the power property to the node
        node.add_property(update_property)

        version_property = HomieProperty(
            id="version",
            name="current version",
            settable=False,
            datatype=STRING
        )

        # Add the power property to the node
        node.add_property(version_property)
        version_property.value = self.otaInitializer.get_version()

        return node

    def update_firmware(self, topic, payload, retained):
        self.logger.info("updating to version {} after next boot!".format(payload))
        if payload == "latest":
            self.otaInitializer.check_for_update_to_install_during_next_reboot()
        else:
            self.otaInitializer.install_version_after_boot(payload)
        machine.reset()

    def run(self):
        # run forever
        self.homie.run_forever()

    def enter_config_mode(self):
        self.logger.info("entering config mode...")
        with open('configMode', "w") as f:
            f.write('config')
        machine.reset()


controller: EspMicroController = None
