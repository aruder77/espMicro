
NETWORK_PROFILES = 'wifi.dat'
MQTT_PROFILE = 'mqtt.dat'

def read_profiles():
    with open(NETWORK_PROFILES) as f:
        lines = f.readlines()
    profiles = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
        profiles[ssid] = password
    return profiles


def write_profiles(profiles):
    lines = []
    for ssid, password in profiles.items():
        lines.append("%s;%s\n" % (ssid, password))
    with open(NETWORK_PROFILES, "w") as f:
        f.write(''.join(lines))


def write_mqtt(mqttServer, mqttUser, mqttPassword, githubRepo):
    lines = []
    lines.append("mqttServer;%s\n" % mqttServer)
    lines.append("mqttUser;%s\n" % mqttUser)
    lines.append("mqttPassword;%s\n" % mqttPassword)
    lines.append("githubRepo;%s\n" % githubRepo)
    with open(MQTT_PROFILE, "w") as f:
        f.write(''.join(lines))


def read_mqtt():
    with open(MQTT_PROFILE) as f:
        lines = f.readlines()
    mqttServer  = lines[0].strip("\n").split(";")[1]
    mqttUser  = lines[1].strip("\n").split(";")[1]
    mqttPassword  = lines[2].strip("\n").split(";")[1]
    githubRepo = lines[3].strip("\n").split(";")[1]
    return (mqttServer, mqttUser, mqttPassword, githubRepo)   