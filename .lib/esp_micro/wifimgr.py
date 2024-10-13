import network
import socket
import ure
import time
import machine
from sys import platform
from esp_micro.config_loader import read_profiles
from esp_micro.config_loader import write_profiles
from esp_micro.config_loader import write_mqtt
from esp_micro.logutil import get_logger

NETWORK_PROFILES = 'wifi.dat'

RP2 = platform == 'rp2'

ap_ssid = "WifiManager"
ap_password = "tayfunulu"
ap_authmode = 3  # WPA2

wlan_ap = network.WLAN(network.AP_IF)
wlan_sta = network.WLAN(network.STA_IF)

server_socket = None

logger = get_logger()

def get_connection():
    """return a working WLAN(STA_IF) instance or None"""

    # First check if there already is any connection:
    if wlan_sta.isconnected():
        logger.info('...connected already.')
        return wlan_sta

    connected = False
    try:
        # ESP connecting to WiFi takes time, wait a bit and try again:
        time.sleep(3)
        if wlan_sta.isconnected():
            return wlan_sta

        # Read known network profiles from file
        profiles = read_profiles()
        #profiles = {}

        # Search WiFis in range
        wlan_sta.active(True)
        networks = wlan_sta.scan()

        AUTHMODE = {0: "open", 1: "WEP", 2: "WPA-PSK",
                    3: "WPA2-PSK", 4: "WPA/WPA2-PSK"}
        for ssid, bssid, channel, rssi, authmode, hidden in sorted(networks, key=lambda x: x[3], reverse=True):
            ssid = ssid.decode('utf-8')
            encrypted = authmode > 0
            logger.info("ssid: %s chan: %d rssi: %d authmode: %s" %
                  (ssid, channel, rssi, AUTHMODE.get(authmode, '?')))
            if encrypted:
                if ssid in profiles:
                    password = profiles[ssid]
                    connected = do_connect(ssid, password)
                else:
                    logger.info("skipping unknown encrypted network")
            if connected:
                break

    except OSError as e:
        logger.error("exception %s" % str(e))

    # start web server for connection manager:
    if not connected:
        connected = start()

    return wlan_sta if connected else None


def do_connect(ssid, password):
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        logger.info("...already connected")
        return None
    logger.info('Trying to connect to %s(%s)...' % (ssid, password))
    wlan_sta.connect(ssid, password)
    for retry in range(100):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        logger.info('Connected. Network config: %s', wlan_sta.ifconfig())
    else:
        logger.info('Failed. Not Connected to: %s', ssid)
    return connected


def send_header(client, status_code=200, content_length=None):
    client.sendall("HTTP/1.0 {} OK\r\n".format(status_code))
    client.sendall("Content-Type: text/html\r\n")
    if content_length is not None:
        client.sendall("Content-Length: {}\r\n".format(content_length))
    client.sendall("\r\n")


def send_response(client, payload, status_code=200):
    content_length = len(payload)
    send_header(client, status_code, content_length)
    if content_length > 0:
        client.sendall(payload)
    client.close()


def handle_root(client):
    wlan_sta.active(True)
    ssids = sorted(ssid.decode('utf-8') for ssid, *_ in wlan_sta.scan())
    send_header(client)
    client.sendall("""\
        <html>
            <h1 style="color: #5e9ca0; text-align: center;">
                <span style="color: #ff0000;">
                    Wi-Fi Client Setup
                </span>
            </h1>
            <form action="configure" method="post">
                <table style="margin-left: auto; margin-right: auto;">
                    <tbody>
    """)
    while len(ssids):
        ssid = ssids.pop(0)
        client.sendall("""\
                        <tr>
                            <td colspan="2">
                                <input type="radio" name="ssid" value="{0}" />{0}
                            </td>
                        </tr>
        """.format(ssid))
    client.sendall("""\
                        <tr>
                            <td>Password:</td>
                            <td><input name="password" type="password" /></td>
                        </tr>
                        <tr>
                            <td>MQTT server:</td>
                            <td><input name="mqttServer" type="text" /></td>
                        </tr>
                        <tr>
                            <td>MQTT user:</td>
                            <td><input name="mqttUser" type="text" /></td>
                        </tr>
                        <tr>
                            <td>MQTT password:</td>
                            <td><input name="mqttPassword" type="password" /></td>
                        </tr>
                        <tr>
                            <td>Github Repo:</td>
                            <td><input name="githubRepo" type="text" /></td>
                        </tr>
                        <tr>
                            <td>install new versions automatically</td>
                            <td><input type="checkbox" id="autoUpdate" name="autoUpdate" checked></td>
                        </tr>
                        <tr>
                            <td>install development versions</td>
                            <td><input type="checkbox" id="unstableVersions" name="unstableVersions"></td>
                        </tr>
                    </tbody>
                </table>
                <p style="text-align: center;">
                    <input type="submit" value="Submit" />
                </p>
            </form>
            <p>&nbsp;</p>
            <hr />
            <h5>
                <span style="color: #ff0000;">
                    Your ssid and password information will be saved into the
                    "%(filename)s" file in your ESP module for future usage.
                    Be careful about security!
                </span>
            </h5>
            <hr />
            <h2 style="color: #2e6c80;">
                Some useful infos:
            </h2>
            <ul>
                <li>
                    Original code from <a href="https://github.com/cpopp/MicroPythonSamples"
                        target="_blank" rel="noopener">cpopp/MicroPythonSamples</a>.
                </li>
                <li>
                    This code available at <a href="https://github.com/tayfunulu/WiFiManager"
                        target="_blank" rel="noopener">tayfunulu/WiFiManager</a>.
                </li>
            </ul>
        </html>
    """ % dict(filename=NETWORK_PROFILES))
    client.close()


def handle_configure(client, request):
    match = ure.search(
        "ssid=([^&]*)&password=([^&]*)&mqttServer=([^&]*)&mqttUser=([^&]*)&mqttPassword=([^&]*)&githubRepo=([^&]*)(.*)", request)

    if match is None:
        send_response(client, "Parameters not found", status_code=400)
        return False
    # version 1.9 compatibility
    try:
        ssid = match.group(1).decode(
            "utf-8").replace("%3F", "?").replace("%21", "!")
        password = match.group(2).decode(
            "utf-8").replace("%3F", "?").replace("%21", "!")
        mqttServer = match.group(3).decode(
            "utf-8").replace("%3F", "?").replace("%21", "!")
        mqttUser = match.group(4).decode(
            "utf-8").replace("%3F", "?").replace("%21", "!")
        mqttPassword = match.group(5).decode(
            "utf-8").replace("%3F", "?").replace("%21", "!")
        githubRepo = match.group(6).decode(
            "utf-8").replace("%3F", "?").replace("%21", "!").replace("%3A", ":").replace("%2F", "/")
        rest = match.group(7).decode(
            "utf-8").replace("%3F", "?").replace("%21", "!")
        autoUpdate = "autoUpdate" in rest
        unstableVersions = "unstableVersions" in rest

        logger.info('mqttServer: ' + mqttServer)
        logger.info('mqttUser: ' + mqttUser)
        logger.info('mqttPassword: ' + mqttPassword)
        if autoUpdate:
            logger.info('autoUpdate!')
        if unstableVersions:
            logger.info('unstableVersions!')

    except Exception:
        ssid = match.group(1).replace("%3F", "?").replace("%21", "!")
        password = match.group(2).replace("%3F", "?").replace("%21", "!")

    if len(ssid) == 0:
        send_response(client, "SSID must be provided", status_code=400)
        return False

    if do_connect(ssid, password):
        try:
            profiles = read_profiles()
        except OSError:
            profiles = {}
        profiles[ssid] = password
        write_profiles(profiles)

        response = """\
            <html>
                <center>
                    <br><br>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP successfully connected to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                </center>
            </html>
        """ % dict(ssid=ssid)
        logger.info('Responding to client...')
        send_response(client, response)
        write_mqtt(mqttServer, mqttUser, mqttPassword,
                   githubRepo, autoUpdate, unstableVersions)

        time.sleep(10)

        machine.reset()
        return True
    else:
        response = """\
            <html>
                <center>
                    <h1 style="color: #5e9ca0; text-align: center;">
                        <span style="color: #ff0000;">
                            ESP could not connect to WiFi network %(ssid)s.
                        </span>
                    </h1>
                    <br><br>
                    <form>
                        <input type="button" value="Go back!" onclick="history.back()"></input>
                    </form>
                </center>
            </html>
        """ % dict(ssid=ssid)
        send_response(client, response)
        return False


def handle_not_found(client, url):
    send_response(client, "Path not found: {}".format(url), status_code=404)


def stop():
    global server_socket

    if server_socket:
        server_socket.close()
        server_socket = None


def start(port=80):
    global server_socket

    addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]

    stop()

    if RP2:
        wlan_ap.config(essid=ap_ssid, password=ap_password)
    else:
        wlan_ap.config(essid=ap_ssid, password=ap_password,
                       authmode=ap_authmode)

    wlan_sta.active(True)
    wlan_ap.active(True)

    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(1)

    logger.info('Connect to WiFi ssid ' + ap_ssid +
          ', default password: ' + ap_password)
    logger.info('and access the ESP via your favorite web browser at 192.168.4.1.')
    logger.info('Listening on: %s' % str(addr))

    while True:
        if wlan_sta.isconnected():
            return True

        client, addr = server_socket.accept()
        logger.info('client connected from %s' % str(addr))
        try:
            client.settimeout(5.0)

            request = b""
            try:
                while "\r\n\r\n" not in request:
                    request += client.recv(512)
            except OSError:
                pass

            logger.info("Request is: {}".format(request))
            if "HTTP" not in request:  # skip invalid requests
                continue

            # version 1.9 compatibility
            try:
                url = ure.search("(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP",
                                 request).group(1).decode("utf-8").rstrip("/")
            except Exception:
                url = ure.search(
                    "(?:GET|POST) /(.*?)(?:\\?.*?)? HTTP", request).group(1).rstrip("/")
            logger.info("URL is {}".format(url))

            if url == "":
                handle_root(client)
            elif url == "configure":
                handle_configure(client, request)
            else:
                handle_not_found(client, url)

        finally:
            client.close()
