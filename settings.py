# Debug mode disables WDT, print mqtt messages
# DEBUG = False

###
# MQTT settings
###

# Defines the mqtt connection timemout in seconds
# MQTT_KEEPALIVE = 30

# SSL connection to the broker. Some MicroPython implementations currently
# have problems with receiving mqtt messages over ssl connections.
# MQTT_SSL = False
# MQTT_SSL_PARAMS = {}
# MQTT_SSL_PARAMS = {"do_handshake": True}

# Base mqtt topic the device publish and subscribes to, without leading slash.
# Base topic format is bytestring.
MQTT_BASE_TOPIC = "devices"


###
# Device settings
###

# The device ID for registration at the broker. The device id is also the
# base topic of a device and must be unique and bytestring.
# from homie.utils import get_unique_id
DEVICE_ID = "microhomie1"

# Friendly name of the device as bytestring
DEVICE_NAME = "microhomie1"

# Time in seconds the device updates device properties
# DEVICE_STATS_INTERVAL = 60

# Subscribe to broadcast topic is enabled by default. To disable broadcast
# messages set BROADCAST to False
# BROADCAST = True

# Enable build-in extensions
from homie.constants import EXT_MPY, EXT_FW, EXT_STATS
EXTENSIONS = [
    EXT_MPY,
    EXT_FW,
    EXT_STATS,
]
