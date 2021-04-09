def connectToWifiAndUpdate():
    import time, machine, network, gc
    time.sleep(1)
    print('Memory free', gc.mem_free())

    from ota_updater import OTAUpdater

    sta_if = network.WLAN(network.STA_IF)
    print('network config:', sta_if.ifconfig())
    otaUpdater = OTAUpdater('https://github.com/aruder77/espMicro', main_dir='app')
    hasUpdated = otaUpdater.install_update_if_available()
    if hasUpdated:
        machine.reset()
    else:
        del(otaUpdater)
        gc.collect()

def startApp():
    import app.start


def main():
    wlan = wifimgr.get_connection()
    if wlan is None:
        print("Could not initialize the network connection.")
        while True:
            pass  # you shall not pass :D

    connectToWifiAndUpdate()
    startApp()        




if __name__ == "__main__":
    main()
