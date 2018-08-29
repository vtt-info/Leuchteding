import network, utime

def connect():

    STA_SSID = "deine-ssid"
    STA_PSK  = "dein-passwort"
    ssid = "esp32"
    pw = "HuchEinPw"
    hostname = "RainbowWarrior"

    ap_if = network.WLAN(network.AP_IF)
    sta_if = network.WLAN(network.STA_IF)

    sta_if.active()
    sta_if.connect(STA_SSID, STA_PSK)

    #try to connect to the router for a while. if no connection was established abort
    timeout = 50
    while not sta_if.isconnected():
        utime.sleep_ms(100)
        timeout -= 1
        if timeout == 0:
            break

    #if connection was established print configurations
    if sta_if.isconnected():
        print("======= STA connected ========")
        print(sta_if.ifconfig())

    #create accesspoint with given credentials
    print("creating accesspoint")
    ap_if.active(True)
    ap_if.config(essid = ssid, password = pw)

    # wait until started and print configurationsself.
    # isconnected(False) means we don't have to wait until a client has connected
    timeout = 50
    while not ap_if.isconnected(False):
        utime.sleep_ms(100)
        timeout -= 1
        if timeout == 0:
            break
    print("======= AP connected ========")
    print(ap_if.ifconfig)

    # to access the webpage via hostname instead of ip adress, we need to create a mDNS instance
    # host will be printed if it was successfull
    try:
        mdns = network.mDNS()
        mdns.start(hostname, "MicroPython with mDNS")
        mdns.addService('_http', '_tcp', 80, "MicroPython", {"board": "ESP32", "service": "mPy Web server"})
        print("webpage available under {}.local".format(hostname))
    except:
        print("mDNS not started")